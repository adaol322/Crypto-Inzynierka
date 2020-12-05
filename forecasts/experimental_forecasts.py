from base.base_forecasts import BaseForecasts
from utils.utils import invert_data_transformations
import numpy as np


class ExperimentalForecasts(BaseForecasts):
    def __init__(self, model, data_loader, config):
        super(ExperimentalForecasts, self).__init__(data_loader, config)
        self.model = model
        self.batch_size = self.config.trainer.batch_size
        #       tuple -> self.X_test = self.test_data[0], self.y_test = self.test_data[1]
        self.test_data = self.data_loader.get_test_data()
        self.forecasts_rescaled = []

    def forecast_with_model(self):
        self.forecasts_scaled = self.model.predict(
            self.test_data[0],
            batch_size=self.config.trainer.batch_size,
            verbose=self.config.trainer.verbose_training
        )
        test_differential = self.data_loader.data_transformer.reverse_transform(self.forecasts_scaled)
        test_raw = self.data_loader.get_test_plot_values()
        test_calculated = self.calculate_predicted(test_raw, test_differential)
        return test_raw, test_calculated

    def calculate_predicted(self, test_raw, test_differential):
        test_calculated = []
        for i in range(0, len(test_differential)):
            temp = test_raw[i] + test_differential[i]
            test_calculated.append(temp)
        test_calculated = np.array(test_calculated)
        return test_calculated

    def forecast_without_model(self):
        print("LSTM must have a model!")
