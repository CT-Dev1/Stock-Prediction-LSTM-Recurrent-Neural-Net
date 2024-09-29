This project generated a final Latex-coded report on a custom made long-short term memory recurrent neural network trained for short-term stock price prediction.

This project involved training, cross-validating and optimizing hyperparameters for the neural network specification, comparing between available architectures. It achieved a mark of 70% (1:1) as the final project for my Artificial Intelligence class in the Statistics Department.

Code utilizes pandas, tensorflow, keras, scikit-learn and other similar packages for training and deployment. The final model achieves a reasonable accuracy of 73% on the testing data on a simplified up/down price movement test. This is deemed a successful model given the stochastic and unpredictable nature of stock price movements.  

Single-input_RNNLSTM.ipynb - This is a proof of concept of the training and testing strategy by focusing on a single stock, model loss and accuracy are measured following training on unseen test data.

multi_stock_mdoel.ipynb - This extends the approach in the single input to a set of stocks to generalize the model and prevent overfitting. This generates the final model for price prediction. Diagnostics on model performance are evaluated. 

Other files were for data transformation and experimentation, these can be generally ignored. 
