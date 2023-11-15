import time
import pygame
import os



pygame.font.init()
pygame.mixer.init()

Ventana = pygame.display.set_mode( ( 800, 600 ) )
miFuente = pygame.font.SysFont( "System", 60 )
WIDTH, HEIGHT = 800, 600
Negro = ( 0, 0, 0 )
Blanco = ( 255, 255, 255 )
Magenta = ( 255, 0, 127 )
Cian = ( 0, 255, 255 )
Gris = ( 103, 103, 103 )
BORDER = pygame.Rect(WIDTH, 0, 10, HEIGHT)

BULLET_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

def Inicio():
    Presentacion=pygame.image.load("principal.png")
    Ventana.blit(Presentacion,(0,0))
    pygame.display.update()
    time.sleep(2)
    Menu()

def Ayuda():
    Ayuda=pygame.image.load("ayuda.png")
    Ventana.blit(Ayuda,(0,0))
    pygame.display.update()
    while True:
        for Eventos in pygame.event.get():
            if Eventos.type == pygame.QUIT:
                Menu()

def Menu():
    Menu=pygame.image.load("inicio.png")
    Ventana.blit(Menu,(0,0))
    pygame.display.update()
    while True:
        for Eventos in pygame.event.get():
            if Eventos.type == pygame.QUIT:
                exit()
            if Eventos.type == pygame.MOUSEBUTTONDOWN:
                x,y = Eventos.pos
                if (x>=58 and y>=170 and x<=279 and y<=234):
                    batalla()
                if (x>=58 and y>=251 and x<=299 and y<=315):
                    Ayuda()
                if (x>=58 and y>=330 and x<=226 and y<=396):
                    exit()
        Ventana.blit(Menu,(0,0))
        pygame.display.update()

def draw_winner(text):
    draw_text = miFuente.render( text, 1, Magenta )
    Ventana.blit( draw_text, ( 800/2 - draw_text.get_width() / 2, 450/2 - draw_text.get_height()/2 ) )
    pygame.display.update()
    pygame.time.delay( 5000 )

#Esta función se encarga del movimiento de las balas, de la colisión de éstas
#y de eliminarlas cuando se salen de la pantalla
def handle_bullets( balas_amarillas, balas_rojas, jugador1, jugador2, aux ):
    for bullet in balas_amarillas:
        bullet.y += BULLET_VEL
        if jugador2.colliderect(bullet):
            pygame.event.post(pygame.event.Event( RED_HIT ) )
            balas_amarillas.remove( bullet )

        elif bullet.y > 600:
            balas_amarillas.remove( bullet )
    
    for bullet in balas_rojas:
        bullet.x += BULLET_VEL*aux
        if jugador1.colliderect( bullet ):
            pygame.event.post( pygame.event.Event( YELLOW_HIT ) )
            balas_rojas.remove( bullet )
        
        elif bullet.x < 0 or bullet.x >800:
            balas_rojas.remove( bullet )
    

def batalla():
    pygame.init()
    pygame.mixer.init()

    imgFondo = pygame.image.load( "fondo.png" )	
    sonidoImpacto = pygame.mixer.Sound( "Grenade.wav" )
    sonidoBala = pygame.mixer.Sound( "Shot.wav" )
    fondoaud = pygame.mixer.Sound( "fondo.wav" )

    vidasJugador1 = 10
    vidasJugador2 = 10
    #Colores
    
    PlayerAncho = 100
    PlayerAlto = 110
    clock = pygame.time.Clock()

    #Coordenadas y velocidad del jugador 1
    CoorPlayer1_X = 400
    CoorPlayer1_Y = 50
    player1Vel_Y = 4
    player1Vel_X = 4

    #Coordenadas y velocidad del jugador 2
    CoorPlayer2_X = 400
    CoorPlayer2_Y = 300 - 45
    Player2Vel_X = 0

    cont = 0
    cont2 = 0

    game_over = False

    balas_rojas = []
    balas_amarillas = []
    direc = 0
    aux = 0
    flag2 = 2
    imgJugador2 = pygame.image.load( os.path.join( 'rojo1-2.png' ) )
    imgJugador1 = pygame.image.load( os.path.join( 'amarillo1.png' ) )
    logo = pygame.image.load( os.path.join( 'logo.png' ) )
    logo2 = pygame.image.load( os.path.join( 'logo2.png' ) )
    pygame.mixer.Sound.play( fondoaud )

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.stop(fondoaud)
                Menu()
            if event.type == pygame.KEYDOWN:
                
                # Jugador 2
                if event.key == pygame.K_LEFT:
                    Player2Vel_X = -3
                    imgJugador2 = pygame.image.load( os.path.join( 'rojo2-2.png' ) )
                    flag2 = 2
                if event.key == pygame.K_RIGHT:
                    Player2Vel_X = 3
                    imgJugador2 = pygame.image.load( os.path.join( 'rojo2.png' ) )
                    flag2 = 1

                if ( event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT) and len( balas_amarillas ) < MAX_BULLETS and cont<6:
                    bullet = pygame.Rect( jugador1.x + jugador1.width, jugador1.y + jugador1.height//2 - 30, 40, 40 )
                    balas_amarillas.append( bullet )
                    pygame.mixer.Sound.play( sonidoBala )
                    cont += 1

                
                
                #Se utilizan dos // en la división para que el resultado sea un número entero
                if event.key == pygame.K_LCTRL and len( balas_rojas ) < MAX_BULLETS:
                    bullet = pygame.Rect( jugador2.x, jugador2.y + jugador2.height//2 - 15, 20, 20 )
                    balas_rojas.append( bullet )
                    pygame.mixer.Sound.play( sonidoBala )
                    cont2 += 1
                    if direc == 0:
                        aux = -1
                    else:
                        aux = 1
            
            if event.type == pygame.KEYUP:
                # Jugador 2
                if event.key == pygame.K_LEFT:
                    Player2Vel_X = 0
                    imgJugador2 = pygame.image.load( os.path.join( 'rojo1-2.png' ) )
                    direc = 0
                if event.key == pygame.K_RIGHT:
                    Player2Vel_X = 0
                    imgJugador2 = pygame.image.load( os.path.join( 'rojo1.png' ) )
                    direc = 1
                
            if event.type == RED_HIT:
                vidasJugador2 -= 1
                pygame.mixer.Sound.play( sonidoImpacto )

            if event.type == YELLOW_HIT:
                vidasJugador1 -= 1
                pygame.mixer.Sound.play( sonidoImpacto )

            

        winner_text = ""

        
        
        Ventana.blit( imgFondo, ( 0, 0 ) )
        
        #Zona de dibujo
        jugador1 = pygame.draw.rect( Ventana, Gris, ( CoorPlayer1_X+20, CoorPlayer1_Y+20, PlayerAncho-40, PlayerAlto-40 ), 1, 100 )
        
        jugador2 = pygame.draw.rect( Ventana, Gris, ( CoorPlayer2_X, CoorPlayer2_Y, PlayerAncho-60, PlayerAlto+45 ), 1 )
        
        # Modifica las coordenadas para dar mov. a los jugadores/ pelota
        
        if CoorPlayer1_X > 30:
            CoorPlayer1_X += player1Vel_X
        else:
            player1Vel_X *= -1
            CoorPlayer1_X += player1Vel_X
        if CoorPlayer1_X < 700:
            CoorPlayer1_X += player1Vel_X
        else:
            player1Vel_X *= -1
            CoorPlayer1_X += player1Vel_X
        if cont == 6:
            if CoorPlayer1_Y < 300-45:
                CoorPlayer1_Y += player1Vel_Y
            else:
                CoorPlayer1_Y = 300-45
                imgJugador1 = pygame.image.load( os.path.join( 'amarillo1-2.png' ) )
            if cont2 == 3:
                cont = 0
                cont2 = 0
        else:
            if CoorPlayer1_Y > 50:
                CoorPlayer1_Y -= player1Vel_Y
                imgJugador1 = pygame.image.load( os.path.join( 'amarillo1.png' ) )

        if CoorPlayer2_X < 750:
            CoorPlayer2_X += Player2Vel_X
        elif CoorPlayer2_X >= 750:
            CoorPlayer2_X -= 3
        if CoorPlayer2_X > 20:
            CoorPlayer2_X += Player2Vel_X
        elif CoorPlayer2_X <= 20:
            CoorPlayer2_X += 3

        
        Ventana.blit( imgJugador1, ( CoorPlayer1_X-20, CoorPlayer1_Y ) )

        if flag2 == 1:
            Ventana.blit( imgJugador2, ( CoorPlayer2_X-25, CoorPlayer2_Y ) )
        elif flag2 == 2:
            Ventana.blit( imgJugador2, ( CoorPlayer2_X-50, CoorPlayer2_Y ) )

        Ventana.blit( logo, (20,0) )
        Ventana.blit( logo2, (700,0) )
        MarcadorJugador1 = miFuente.render( str( vidasJugador1 ), False, Magenta )
        MarcadorJugador2 = miFuente.render( str( vidasJugador2 ), False, Cian )
        Ventana.blit( MarcadorJugador1, ( 100, 10 ) )
        Ventana.blit( MarcadorJugador2, ( 665, 10 ) )

        for bullet in balas_rojas:
            pygame.draw.rect( Ventana, Cian, bullet, 0, 100 )

        for bullet in balas_amarillas:
            pygame.draw.rect( Ventana, Magenta, bullet, 0, 100 )
    
        winner_text = ""
        if vidasJugador2 <= 0:
            winner_text = "Perdiste!"
            imgJugador2 = pygame.image.load( os.path.join( 'perdiste1.png' ) )
            Ventana.blit( imgFondo, ( 0, 0 ) )
            Ventana.blit( imgJugador2, ( CoorPlayer2_X-50, CoorPlayer2_Y+95) )
            imgJugador2 = pygame.image.load( os.path.join( 'perdiste.png' ) )
            Ventana.blit( imgJugador2, ( CoorPlayer2_X-50, CoorPlayer2_Y ) )
            Ventana.blit( imgJugador1, ( CoorPlayer1_X-20, CoorPlayer1_Y ) )
            Ventana.blit( logo, (20,0) )
            Ventana.blit( logo2, (700,0) )
            MarcadorJugador1 = miFuente.render( str( vidasJugador1 ), False, Magenta )
            MarcadorJugador2 = miFuente.render( str( vidasJugador2 ), False, Cian )
            Ventana.blit( MarcadorJugador1, ( 100, 10 ) )
            Ventana.blit( MarcadorJugador2, ( 665, 10 ) )
            

        if vidasJugador1 <= 0:
            winner_text = "Ganaste!"
            

        if winner_text != "":
            draw_winner( winner_text )
            pygame.display.flip()
            time.sleep(3)
            break

        handle_bullets( balas_amarillas, balas_rojas, jugador1, jugador2, aux )

        pygame.display.flip()
        clock.tick( 60 )
    pygame.mixer.Sound.stop(fondoaud)
    Menu()

if __name__=='__main__':
    Inicio()