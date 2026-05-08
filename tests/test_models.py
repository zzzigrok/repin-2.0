import unittest
import torch
from cli import Discriminator, Generator, image_size, latent_size

class TestModels(unittest.TestCase):
    def test_generator_forward(self):
        """
        Test the Generator model's forward pass.
        Asserts the output shape is (batch_size, image_size).
        """
        batch_size = 16
        model = Generator()
        # latent_size is 64
        dummy_input = torch.randn(batch_size, latent_size)

        output = model(dummy_input)

        # Check output shape
        self.assertEqual(output.shape, (batch_size, image_size))

        # Check output values (should be between -1 and 1 due to Tanh)
        self.assertTrue(torch.all(output >= -1))
        self.assertTrue(torch.all(output <= 1))

    def test_discriminator_forward(self):
        """
        Test the Discriminator model's forward pass.
        Asserts the output shape is (batch_size, 1) and values are between 0 and 1.
        """
        batch_size = 16
        model = Discriminator()
        # image_size is 784 (28*28)
        dummy_input = torch.randn(batch_size, image_size)

        output = model(dummy_input)

        # Check output shape
        self.assertEqual(output.shape, (batch_size, 1))

        # Check output values (should be between 0 and 1 due to Sigmoid)
        self.assertTrue(torch.all(output >= 0))
        self.assertTrue(torch.all(output <= 1))

if __name__ == '__main__':
    unittest.main()
