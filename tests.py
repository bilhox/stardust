import random

def main():
     done = False
     while not done:
          
          a = input("Lancer un tirage au sort (O = lancement du tirage , E = exit)")
          
          if a == "O":
               print(random.randint(1,5))
          elif a == "E":
               done = True
          


if __name__ == "__main__":
     main()