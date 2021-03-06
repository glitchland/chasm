# -*- coding: utf-8 -*-

import unittest
from chasm import lexical, errors

logger = errors.Logger()


class TokenizerTestCase(unittest.TestCase):

    def tearDown(self):
        logger.clear()

    def test_tokenize_comment(self):

        # Arrange:
        code = "; CHIP8 Assembler\n"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_COMMENT', tokens[0]['class'])
        self.assertEqual('; CHIP8 Assembler', tokens[0]['lexeme'])

        self.assertEqual('T_EOL', tokens[1]['class'])

    def test_tokenize_whitespace(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_WHITESPACE', tokens[1]['class'])
        self.assertEqual(' ', tokens[1]['lexeme'])

    def test_tokenize_eol(self):

        # Arrange:
        code = "Start:\n  ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_EOL', tokens[1]['class'])
        self.assertEqual('\n', tokens[1]['lexeme'])

    def test_tokenize_name(self):

        # Arrange:
        code = "JMP Draw"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_NAME', tokens[2]['class'])
        self.assertEqual('Draw', tokens[2]['lexeme'])

    def test_tokenize_comma(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_COMMA', tokens[3]['class'])
        self.assertEqual(',', tokens[3]['lexeme'])

    def test_tokenize_command(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_COMMAND', tokens[0]['class'])
        self.assertEqual('ADD', tokens[0]['lexeme'])

    def test_tokenize_addr(self):

        # Arrange:
        code = "JMP #FFF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_CONSTANT', tokens[2]['class'])
        self.assertEqual('#FFF', tokens[2]['lexeme'])

    def test_tokenize_byte(self):

        # Arrange:
        code = "ADD V0, 239"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_NUMBER', tokens[5]['class'])
        self.assertEqual('239', tokens[5]['lexeme'])

    def test_tokenize_nibble(self):

        # Arrange:
        code = "DRW V0, V1, 15"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_NUMBER', tokens[8]['class'])
        self.assertEqual('15', tokens[8]['lexeme'])

    def test_tokenize_register(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_REGISTER', tokens[2]['class'])
        self.assertEqual('V0', tokens[2]['lexeme'])

    def test_tokenize_label(self):

        # Arrange:
        code = "Start:\n    ADD V0, 0xFF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_LABEL', tokens[0]['class'])
        self.assertEqual('Start:', tokens[0]['lexeme'])

    def test_tokenize_delay_timer(self):

        # Arrange:
        code = "LD V0, DT"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_DELAY', tokens[5]['class'])

    def test_tokenize_sound_timer(self):

        # Arrange:
        code = "LD ST, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_SOUND', tokens[2]['class'])

    def test_tokenize_registerI(self):

        # Arrange:
        code = "LD I, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_REGISTER_I', tokens[2]['class'])

    def test_tokenize_font(self):

        # Arrange:
        code = "LD F, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_FONT', tokens[2]['class'])

    def test_tokenize_keyboard(self):

        # Arrange:
        code = "LD V0, K"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_KEYBOARD', tokens[5]['class'])

    def test_tokenize_binary(self):

        # Arrange:
        code = "LD B, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_BINARY', tokens[2]['class'])

    def test_tokenize_value(self):

        # Arrange:
        code = "LD V1, 2"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_NUMBER', tokens[5]['class'])

    def test_throw_exception_with_has_error_characters(self):

        # Arrange:
        code = "ADD #V0, 0xFF"

        # Act:
        lexical.tokenize(code)

        # Assert:
        self.assertTrue(logger.has_error)

    def test_show_column_from_asm(self):

        # Arrange:
        code = "ADD V0, #FF\nLD V0, #FE"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual(1, tokens[0]['column'])
        self.assertEqual(5, tokens[2]['column'])
        self.assertEqual(1, tokens[7]['column'])

    def test_show_line_from_asm(self):

        # Arrange:
        code = "ADD V0, #FF\nLD V0, #FE"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual(1, tokens[0]['line'])
        self.assertEqual(2, tokens[7]['line'])
