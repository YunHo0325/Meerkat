from tensorflow.keras.models import load_model
model = load_model("C:/Users/dbsgh/Desktop/hackathon/model/model.h5")


from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot


SVG(model_to_dot(model, show_shapes=True).create(prog='dot', format='svg'))