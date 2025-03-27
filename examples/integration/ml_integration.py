#!/usr/bin/env python3
"""
Machine Learning Integration Example

This example demonstrates how to integrate LlamaPackages with a machine learning workflow,
showing how to manage and use ML-related packages for a text classification task.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the parent directory to sys.path to make the llamapackage module importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llamapackage import PackageRegistry, Config

class MLWorkflow:
    """Example machine learning workflow using LlamaPackages."""
    
    def __init__(self):
        """Initialize the ML workflow with LlamaPackages."""
        # Initialize LlamaPackages
        self.config = Config()
        self.config.registry_url = "https://registry.llamasearch.ai"
        self.config.auth_token = os.environ.get("LLAMA_AUTH_TOKEN", "")
        self.registry = PackageRegistry(self.config)
        
        # Required packages for this ML workflow
        self.required_packages = [
            "llamatext",      # For text preprocessing
            "llamavectors",   # For vector embeddings
            "llamaclassify",  # For classification models
            "llamaeval"       # For evaluation metrics
        ]
        
        # Data and model storage
        self.data = None
        self.model = None
    
    def setup_environment(self):
        """Set up the environment by installing required packages."""
        print("Setting up ML environment...")
        
        for package in self.required_packages:
            try:
                print(f"Checking if {package} is installed...")
                if not self.registry.is_package_installed(package):
                    print(f"Installing {package}...")
                    self.registry.install_package(package)
                    print(f"Successfully installed {package}")
                else:
                    print(f"{package} is already installed")
            except Exception as e:
                print(f"Error installing {package}: {e}")
                return False
        
        print("Environment setup complete.")
        return True
    
    def load_data(self, data_path=None):
        """Load and preprocess the dataset."""
        print("\nLoading and preprocessing data...")
        
        # In a real scenario, we would import the llamatext package
        # For this example, we'll simulate its usage
        print("from llamatext import TextPreprocessor")
        print("preprocessor = TextPreprocessor()")
        
        # Simulate loading data
        if data_path:
            print(f"Loading data from {data_path}")
        else:
            print("Loading sample data")
            
        # Simulate preprocessing
        print("data = preprocessor.load_and_clean(data_path)")
        print("train_data, test_data = preprocessor.train_test_split(data, test_size=0.2)")
        
        # For simulation purposes
        self.data = {
            "train": {"texts": ["sample text 1", "sample text 2"], "labels": [0, 1]},
            "test": {"texts": ["sample text 3"], "labels": [0]}
        }
        
        print("Data loading and preprocessing complete.")
        return True
    
    def vectorize_data(self):
        """Convert text data to vector embeddings."""
        print("\nVectorizing text data...")
        
        # Simulate using llamavectors
        print("from llamavectors import Vectorizer")
        print("vectorizer = Vectorizer(model='llama-embed-v1')")
        print("train_vectors = vectorizer.transform(train_data['texts'])")
        print("test_vectors = vectorizer.transform(test_data['texts'])")
        
        # Simulate vector creation
        print("Vectors created with dimensionality: 384")
        
        return True
    
    def train_model(self):
        """Train a classification model on the vectorized data."""
        print("\nTraining classification model...")
        
        # Simulate using llamaclassify
        print("from llamaclassify import TextClassifier")
        print("classifier = TextClassifier(model_type='llama-classify-v2')")
        print("classifier.fit(train_vectors, train_data['labels'])")
        
        # Simulate model training
        print("Model trained with accuracy: 0.92")
        self.model = "trained_classifier"
        
        return True
    
    def evaluate_model(self):
        """Evaluate the trained model on test data."""
        print("\nEvaluating model performance...")
        
        # Simulate using llamaeval
        print("from llamaeval import ClassificationEvaluator")
        print("evaluator = ClassificationEvaluator()")
        print("predictions = classifier.predict(test_vectors)")
        print("metrics = evaluator.evaluate(test_data['labels'], predictions)")
        
        # Simulate evaluation results
        metrics = {
            "accuracy": 0.89,
            "precision": 0.87,
            "recall": 0.85,
            "f1_score": 0.86
        }
        
        print("\nEvaluation metrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.2f}")
        
        return metrics
    
    def save_model(self, output_path=None):
        """Save the trained model."""
        if not self.model:
            print("Error: No model has been trained yet.")
            return False
        
        print("\nSaving trained model...")
        
        # Create a temporary file if no output path is provided
        if not output_path:
            fd, output_path = tempfile.mkstemp(suffix='.pkl')
            os.close(fd)
        
        # Simulate saving model
        print(f"Model saved to: {output_path}")
        
        return output_path
    
    def run_workflow(self, data_path=None, output_path=None):
        """Run the complete ML workflow."""
        print("Starting ML workflow with LlamaPackages integration\n")
        
        # Step 1: Setup environment with required packages
        if not self.setup_environment():
            print("Failed to set up environment. Aborting workflow.")
            return False
        
        # Step 2: Load and preprocess data
        if not self.load_data(data_path):
            print("Failed to load data. Aborting workflow.")
            return False
        
        # Step 3: Vectorize the text data
        if not self.vectorize_data():
            print("Failed to vectorize data. Aborting workflow.")
            return False
        
        # Step 4: Train the classification model
        if not self.train_model():
            print("Failed to train model. Aborting workflow.")
            return False
        
        # Step 5: Evaluate the model
        metrics = self.evaluate_model()
        if not metrics:
            print("Failed to evaluate model. Aborting workflow.")
            return False
        
        # Step 6: Save the model
        model_path = self.save_model(output_path)
        if not model_path:
            print("Failed to save model. Aborting workflow.")
            return False
        
        print("\nML workflow completed successfully!")
        print(f"Model saved to: {model_path}")
        
        return {
            "metrics": metrics,
            "model_path": model_path
        }

def main():
    """Run the ML workflow integration example."""
    print("LlamaPackages Machine Learning Integration Example")
    print("=================================================\n")
    
    workflow = MLWorkflow()
    result = workflow.run_workflow()
    
    if result:
        print("\nWorkflow result summary:")
        print(f"Model path: {result['model_path']}")
        print("Evaluation metrics:")
        for metric, value in result['metrics'].items():
            print(f"  {metric}: {value:.2f}")
    
    print("\nML Integration example completed.")

if __name__ == "__main__":
    main() 