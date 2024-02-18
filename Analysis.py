from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import logging
import pandas as pd
from datetime import datetime


class Analysis():

    def __init__(self, analysis_config: str):
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        self.config = config
        self.data = None
        logging.basicConfig(level=logging.INFO)

    def load_data(self):
        '''
        Description 
        -----------
        Load system-wide and user configuration files.

        Parameters
        ----------
        Extract the 'api_key' and 'username' from the system-config file

        Returns
        -------
        dict
            The consolidated data of all the repositories with creation date from Github account
        '''
        Github_token = self.config.get('api_key')  
        username = self.config.get('username')
        if not Github_token or not username:
            logging.error("API key or username not found in configuration.")
            return
        
        github_api_url = f'https://api.github.com/users/{username}/repos'
        Headers = {'Authorization': f'token {Github_token}'}
        try:
            response = requests.get(github_api_url, headers=Headers)
            data = response.json()
            # Extracting repository name and creation date 
            self.dataset = pd.DataFrame(data)[['name', 'created_at']]
            logging.info("Data loaded successfully")
        except Exception as e:
            logging.error(f"Error loading data from account: {e}")
            raise 

    def compute_analysis(self) -> Any:
        '''
        Analyze the loaded data to count total repositories created each year. 

        Returns
        -------
        pd.Series
            Number of repositories created each year.

        '''
        # Convert 'created_at' to datetime format and sort by it
        self.dataset['created_at'] = pd.to_datetime(self.dataset['created_at'])
        
        # Created a column of 'Published Year' from 'created_at'
        self.dataset['year'] = self.dataset['created_at'].dt.year

        return self.dataset['year'].value_counts().sort_index()

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        '''
        Plot the total number of repositories created each year.
        '''
        year_counts = self.compute_analysis()

        fig, ax = plt.subplots()
        ax.plot(year_counts.index.astype(str), year_counts.values, marker='o')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Repositories')
        ax.set_title('Total Number of Repositories Created Each Year')
        if save_path:
            plt.savefig(save_path)
        return fig

    def notify_done(self, message: str) -> None:
        ''' Notify the user that analysis is complete.

        Send a notification to the user through the ntfy.sh webpush service.

        Parameters
        ----------
        message : str
            Text of the notification to send

        Returns
        -------
        None
        '''
        topic_name = 'dsi_analysis'
        message = 'Repo Analysis asssignment done'

        requests.post(f"https://ntfy.sh/{topic_name}", 
                      data=message.encode(encoding='utf-8'))
        
    