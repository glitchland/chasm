; Note: this source has been modified by David WINTER on 17 SEP 1997
;       (only the syntax changed: it has been converted in CHIPPER)
;
; The source could be optimized to save some bytes, but I didn't wanted
; to modify it since there is no specific interest in this.
;
; NOTE THAT THE ORIGINAL SOURCE HAD SEVERAL ERRORS !!!
;
; ------------------------------------------------------
;
; Author: vervalin@AUSTIN.LOCKHEED.COM (Paul Vervalin)
;
;   register          contents
; ------------------------------------------------------
;    V0        scratch
;    V1        scratch
;    V2        scratch
;    V3        X coordinate of score
;    V4        Y coordinate of score
;    V5        bricks hit counter
;    V6        ball X coordinate
;    V7        ball Y coordinate
;    V8        ball X direction
;    V9        ball Y direction
;    VA        X coordinate when generating bricks
;    VB        Y coordinate when generating bricks
;    VC        paddle X coordinate
;    VD        paddle Y coordinate
;    VE        ball counter
;    VF        collision detect


    LD  VE, 5   ; Set number of balls to 5
    LD  V5, 0   ; Initial number of hit bricks is 0
    LD  VB, 6   ; Set Y position of first brick to draw

Draw_Bricks:
    LD  VA, 0   ; Set X position of first brick to draw

Draw_Brick_Row:
    LD  I, Brick    ; I points on the brick sprite
    DRW VA, VB, 1   ; Draw brick
    ADD VA, 4       ; Move along X to next brick location
    SE  VA, 64      ; If location wrapped goto next row
    JP  Draw_Brick_Row ; Otherwise draw another

    ADD VB, 2       ; Move down Y to next row
    SE  VB, #12     ; If all rows drawn, continue on

    JP  Draw_Bricks ; Otherwise draw next row

    LD  VC, 32      ; Set X location of paddle
    LD  VD, 31      ; Set Y location of paddle
    LD  I,  Paddle  ; Get address of paddle sprite
    DRW VC, VD, 1   ; Draw paddle

    CALL Draw_Score ; Call subroutine to draw score

    LD  V0, 0     ; Set X coord of balls remaining
    LD  V1, 0     ; Set Y coord of balls remaining
    LD  I,  Balls ; I points on balls sprite
    DRW V0, V1, 1 ; Draw 4 of the five balls
    ADD V0, 8     ; Set X location of the 5th ball sprite
    LD  I,  Ball  ; I points on ball sprite
    DRW V0, V1, 1 ; Draw 5th ball

Play:
    LD  V0, #40 ; Set V0 for delay
    LD  DT, V0  ; Set delay timer
Wait:
    LD  V0, DT  ; Check status of delay timer
    SE  V0, 0   ; Skip next if delay timer is 0
    JP  Wait    ; Check again

    RND V6, #0F ; Get random coord for ball start
    LD  V7, 30  ; Set Y coord of ball start
    LD  V8, 1   ; Set X direction to RIGHT
    LD  V9, #FF ; Set Y direction to UP

    LD  I,  Ball  ; I points on single ball sprite
    DRW V6, V7, 1 ; Draw ball

Loop:
    LD  I, Paddle ; Get address of paddle sprite
    DRW VC, VD, 1 ; Draw paddle at loc. VC VD

    LD  V0, 04  ; Set V0 to key 4
    SKNP V0     ; Skip next if key V0 not pressed
    ADD VC, #FE ; Move paddle two pixels left

    LD  V0, 06  ; Set V0 to key 6
    SKNP V0     ; Skip next if key V0 not pressed
    ADD VC, 2   ; Move paddle two pixels right

    LD  V0, #3F ; Set V0 right edge of screen
    AND VC, V0  ; Wrap paddle around if needed
    DRW VC, VD, 1 ; Draw paddle

    LD  I,  Ball   ; Get address of ball sprite
    DRW V6, V7, 1  ; Draw ball
    ADD V6, V8     ; Move ball in X direction by V8
    ADD V7, V9     ; Move ball in Y direction by V9

    LD  V0, 63  ; Set highest X coord.
    AND V6, V0  ; AND ball X pos. with V0

    LD  V1, 31  ; Set highest Y coord
    AND V7, V1  ; AND ball Y pos. with V1

    SNE V7, 31  ; If ball not at bottom, skip
    JP  Bottom  ; Else check for paddle pos


Check_Paddle:
    SNE V6, 0   ; If ball not at left side, skip
    LD  V8, 1   ; Set X direction to RIGHT

    SNE V6, 63  ; If ball not at right side, skip
    LD  V8, #FF ; Set X direction to LEFT

    SNE V7, 0   ; If ball not at top, skip
    LD  V9, 1   ; Set Y direction to DOWN

    DRW V6, V7, 1 ; Draw ball
    SE  VF, 1     ; If there was a collision, skip
    JP  Brick_Untouched

    SNE V7, 31  ; If ball not at bottom skip
    JP  Brick_Untouched

    LD  V0, 5   ; Set V0 for 5 lines at screen top
    SUB V0, V7  ; Check if ball was in this region
    SE  VF, 0   ; If it was not then skip
    JP  Brick_Untouched

    LD  V0, 1   ; There was a collision
    LD  ST, V0  ; So beep

    LD  V0, V6  ; Get X coord of ball
    LD  V1, #FC ; Compute postion of the brick
    AND V0, V1  ; which was hit

    LD  I, Brick    ; I points on brick sprite
    DRW V0, V7, 1   ; Erase brick sprite by drawing
    LD  V0, #FE     ; reverse the Y direction of the
    XOR V9, V0      ; ball sprite

    CALL Draw_Score ; Call subroutine to draw score
    ADD V5, 1       ; Increments bricks hit counter by one
    CALL Draw_Score ; Call subroutine to draw score

    SNE V5, 96   ; If all bricks have not been hit, skip
    JP  Over     ; Else game ends, so stop


Brick_Untouched:
    JP  Loop

Bottom:
    LD  V9, #FF ; Ball is at bottom, so set direction to UP
    LD  V0, V6  ; Get X location of ball
    SUB V0, VC  ; Intersect with paddle
    SE  VF, 1   ; If intersect then skip
    JP  Ball_Lost

    LD  V1, 2       ;
    SUB V0, V1      ; This portion calculates
    SE  VF, 1       ; the direction where the
    JP  Go_Left     ; ball will bounce,
    SUB V0, V1      ; depending on the position
    SE  VF, 1       ; of the ball on the paddle,
    JP  Paddle_Beep ; and the direction it had
    SUB V0, V1      ; before hiting the paddle.
    SE  VF, 1       ;
    JP  Go_Right    ;


Ball_Lost:
    LD  V0, 32 ; Set beep delay
    LD  ST, V0 ; Beep for lost ball

    LD  I, Ball ; I points on ball sprite
    ADD VE, #FF ; Remove 1 from balls counter
    LD  V0, VE  ; Set V0 to ball counter

    ADD V0, V0    ; Compute location of ball to erase
    LD  V1, 0     ; Set Y location of top line
    DRW V0, V1, 1 ; Erase ball from remaining
    SE  VE, 0     ; If no balls remain, skip
    JP  Play      ; Prepare for a new ball to play


Over:
    JP Over


Go_Left:
    ADD V8, #FF ; Make ball go LEFT
    SNE V8, #FE ; If ball was not going left, skip
    LD  V8, #FF  ; Make it go LEFT by 1 not 2
    JP  Paddle_Beep


Go_Right:
    ADD V8, 1   ; Make ball go right
    SNE V8, 2   ; If ball was not going right, skip
    LD  V8,1    ; Make it go RIGHT by 1 not 2


Paddle_Beep:
    LD  V0, 4        ; Set beep time for paddle hit
    LD  ST, V0       ; Turn on beeper
    LD  V9, #FF      ; Set ball direction to UP
    JP  Check_Paddle ; Then, continue playing and check for paddle move


Draw_Score:
    LD  I, Score    ; Set address to BCD score location
    LD  B, V5       ; Store BCD of score
    LD  V2, [I]     ; Read BCD of score in V0...V2
    LD  F, V1       ; Get font for tens value from V1
    LD  V3, 55      ; Set X location of score tens place
    LD  V4, 0       ; Set Y location of score
    DRW V3, V4, 5   ; Draw tens place score #
    ADD V3, 5       ; Set X location of score ones place
    LD  F, V2       ; Get font for ones value from V2
    DRW V3, V4, 5   ; Draw ones place score #
    RET             ; Return


Brick:
    DW #E000 ; Brick sprite


Ball:
    DW #8000 ; Ball sprite


Paddle:
    DW #FC00 ; Paddle sprite


Balls:
    DW #AA00 ; Balls remaining sprite


Score:
    DW #0000 ; Score storage
    DW #0000 ;