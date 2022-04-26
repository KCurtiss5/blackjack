# Text-only Blackjack
### By: Koby Curtiss 
##### <KCurtiss5@gmail.com>
<br>

#### Table of Contents

- [What is Blackjack?](#what-is-blackjack)
- [About the Project](#about-the-project)
- [Goals for the Project](#goals-for-the-project)
- [How to Play](#how-to-play)
- [Have fun and win lots of money!](#have-fun-and-win-lots-of-money)

## What is Blackjack?
Blackjack is a fun gambling game involving deck(s) of cards. It is unique as a casino game due to the fact that with perfect play and desireable table rules, the game can potentially favor the player during certain rounds.
  
  To learn more about blackjack, please see the *[official rules](https://www.blackjack.org/blackjack/how-to-play/)*.
  
  To learn more about blackjack strategy, please see *[blackjack strategy](https://www.blackjack.org/blackjack/strategy/)*.

## About the Project

This codebase is a **highly-customizable** text-only blackjack game designed for a windows and linux environment. It is currently unknown whether the code works in a Mac environment. Customization options include, but are not limited to:
- number of decks 
- rounds played before shuffling deck 
- a minimum bet 
- allowing double down after 3 cards 
- number of hands allowed to split to
- soft/hard 17
- allowing late surrender
- custom player creation options 
- max players at a table 

This package was meant to be utilized both as entertainment and as a learning tool. The customization is critical as it allows for different environment variables when learning the game.

## Goals for the Project

Ideally, the game will continue to progress in efficiency and customization options. The game, if it sees enough attention, will also include AI players. The plan is to have 3 different levels of AI difficulty: "Beginner","Intermediate", and "Perfect". Beginner will play like a beginner where they will make standard mistakes often. Intermediate will have mastered basic blackjack strategy. Perfect will play perfectly by counting cards and playing with perfect strategy based on the count. 

## How to Play

1. Ensure you have the latest version of python installed. To download, please see: https://www.python.org/downloads/.

2. Download the code from the repository via any github supported method. If you need help, please see: *[cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)*.

3. Next, navigate to the directory where you downloaded the repository and navigate into src/. You can ensure that your python installation includes all of the dependencies this codebase uses with:

        pip install -r requirements.txt


4. Playing the game is rather straightforward. Use a command similar to:
   
        python3 blackjack.py
5. When in the menu, interact with the menu by typing in the corresponding number of the action you want to take.
6. When in the game, your actions are limited to "hit", "stand", "double", and "split". Not all of these actions may be usable depending on the rules of blackjack and current game settings.

### Have fun and win lots of money!

![Pokerchips](/assets/poker_chips.jpg)
