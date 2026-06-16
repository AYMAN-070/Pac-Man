import mazegenerator
import inspect

# On passe le Créateur (le constructeur) au Rayon X !
signature = inspect.signature(mazegenerator.MazeGenerator.__init__)
print(f"Il faut créer l'objet EXACTEMENT comme ça : MazeGenerator{signature}")