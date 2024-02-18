import pytest
from Analysis import Analysis
import pandas as pd

def test_load_data():
    """
    Test that load_data correctly loads data into the dataset attribute.
    Since this involves external API calls, consider using a mock response or a test double.
    """
    
    analysis = Analysis('config.yml')
    
    analysis.load_data()
    assert analysis.dataset is not None

def test_compute_analysis():
    """
    Test compute_analysis on a predefined dataset to ensure correct analysis.
    """
    # Prepare a mock dataset
    mock_data = pd.DataFrame({
        'name': ['repo1', 'repo2'],
        'created_at': ['2021-01-01T00:00:00Z', '2022-01-01T00:00:00Z']
    })
    analysis = Analysis('config.yml')
    analysis.dataset = mock_data
    # Convert 'created_at' to datetime format as expected by compute_analysis
    analysis.dataset['created_at'] = pd.to_datetime(analysis.dataset['created_at'])
    
    result = analysis.compute_analysis()
    assert len(result) > 0

def test_plot_data(tmp_path):
    """
    Test plot_data by checking if a file is created at the provided save_path.
    """
    analysis = Analysis('config.yml')
    
    fig = analysis.plot_data(save_path=str(tmp_path / "plot.png"))
    assert (tmp_path / "plot.png").exists()