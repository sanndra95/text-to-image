import matplotlib.pyplot as plt
import numpy as np


# This function is called when the training begins
def on_train_begin(self, logs={}):
    # Initialize the lists for holding the logs and losses
    self.d_loss = []
    self.g_loss = []
    self.logs = []

# This function is called at the end of each epoch
def on_epoch_end(logs={}):
    # Append the logs and losses to the lists
    d_loss=logs['d_loss']
    g_loss=logs['g_loss']
    losses = len(logs['epoch'])

    # Before plotting ensure at least 2 epochs have passed
    if losses > 1:
        # Clear the previous plot
        #clear_output(wait=True)
        N = np.arange(0, losses)

        # You can chose the style of your preference
        # print(plt.style.available) to see the available options
        plt.style.use("seaborn")

        # Plot train loss, train acc, val loss and val acc against epochs passed
        plt.figure()
        plt.plot(N, np.array(d_loss), label="train_g_loss")
        plt.plot(N, np.array(g_loss), label="train_d_loss")
        #plt.title("Training Loss [Epoch {}]".format(epoch))
        plt.xlabel("Epoch #")
        plt.ylabel("Loss")
        plt.legend()
        plt.show()

