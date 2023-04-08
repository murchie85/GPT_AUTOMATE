score_font = pygame.font.Font('freesansbold.ttf', 32) # Load font for displaying score
player1_score = 0 # Set initial score for player 1
player2_score = 0 # Set initial score for player 2

def update_scores(): # Function to update score display
    score1 = score_font.render('Player 1 Score: ' + str(player1_score), True, (255, 255, 255))
    score2 = score_font.render('Player 2 Score: ' + str(player2_score), True, (255, 255, 255))
    screen.blit(score1, (50, 50))
    screen.blit(score2, (screen_width - score2.get_width() - 50, 50))

def display_menu(): # Function to display main menu
    menu_font = pygame.font.Font('freesansbold.ttf', 64) # Load font for main menu text
    menu_title = menu_font.render('PONG MENU', True, (255, 255, 255))
    menu_start = score_font.render('START GAME', True, (255, 255, 255))
    menu_quit = score_font.render('QUIT GAME', True, (255, 255, 255))
    menu_options = [menu_start, menu_quit]

    selected_option = 0 # Initialize selected option to first option
    menu_running = True # Set menu_running flag to True

while True: # Main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN: # Check for key presses
            if event.key == pygame.K_ESCAPE: # Exit game if player presses escape key
                pygame.quit()
                sys.exit()

            if menu_running: # Check if main menu is currently displayed
                if event.key == pygame.K_UP: # Move selection up on menu
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN: # Move selection down on menu
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN: # Select current option on menu
                    if selected_option == 0: # Start new game
                        menu_running = False # Set menu_running flag to False
                        # Reset game variables
                        ball.x = screen_width / 2
                        ball.y = screen_height / 2
                        ball.angle = random.uniform(-math.pi / 4, math.pi / 4)
                        player1.y = (screen_height - player1.height) / 2
                        player2.y = (screen_height - player2.height) / 2
                        player2.speed = 10 # Reset AI paddle speed to default
                        # Reset scores
                        player1_score = 0
                        player2_score = 0

                    elif selected_option == 1: # Quit game
                        pygame.quit()
                        sys.exit()

    if menu_running: # Display main menu if it is currently running
        display_menu()
    else: # Otherwise, display game screen and update game logic
        screen.fill((0, 0, 0))
        update_scores()
        ball.update()
        player1.update()
        player2.update()
        powerup.update()
        pygame.display.update()

        # Check for collision between ball and paddles
        if ball.rect.colliderect(player1.rect):
            ball.bounce(player1)
        elif ball.rect.colliderect(player2.rect):
            ball.bounce(player2)

        # Check for collision between ball and walls
        if ball.y < 0:
            ball.angle = -ball.angle
        elif ball.y > screen_height:
            ball.angle = -ball.angle
        elif ball.x < 0:
            player2_score += 1
            ball.x = screen_width / 2
            ball.y = screen_height / 2
            ball.angle = random.uniform(-math.pi / 4, math.pi / 4)
            powerup.reset()
        elif ball.x > screen_width:
            player1_score += 1
            ball.x = screen_width / 2
            ball.y = screen_height / 2
            ball.angle = random.uniform(-math.pi / 4, math.pi / 4)
            powerup.reset()##JOB_COMPLETE##