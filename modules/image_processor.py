"""
Image processing module for prescription parsing.
Contains functions to enhance, process, and visualize prescription images.
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
import streamlit as st
import math

class ImageProcessor:
    """Class for processing and enhancing prescription images."""
    
    @staticmethod
    def resize_image(image, target_height=1200):
        """
        Resize image to target height while maintaining aspect ratio.
        
        Args:
            image: Image to resize (OpenCV format)
            target_height: Target height in pixels
            
        Returns:
            Resized image
        """
        height, width = image.shape[:2]
        if height == target_height:
            return image
            
        scale_factor = target_height / height
        dim = (int(width * scale_factor), target_height)
        resized = cv2.resize(
            image, 
            dim, 
            interpolation=cv2.INTER_AREA if height > target_height else cv2.INTER_CUBIC
        )
        return resized
    
    @staticmethod
    def convert_to_grayscale(image):
        """Convert image to grayscale if not already."""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    @staticmethod
    def apply_adaptive_threshold(gray_image):
        """Apply adaptive thresholding to handle uneven lighting."""
        return cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
    
    @staticmethod
    def reduce_noise(image):
        """Apply noise reduction to improve image quality."""
        return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
    
    @staticmethod
    def enhance_edges(image):
        """Enhance edges to improve text boundaries."""
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        return cv2.filter2D(image, -1, kernel)
    
    @staticmethod
    def enhance_contrast(image):
        """Increase contrast to make text stand out using PIL."""
        image_pil = Image.fromarray(image)
        enhancer = ImageEnhance.Contrast(image_pil)
        return enhancer.enhance(1.5)  # 1.5 is the contrast factor
    
    @staticmethod
    def display_processing_steps(steps_images, steps_titles):
        """
        Display multiple processing step images with titles in 2 rows.

        Args:
            steps_images: List of images to display
            steps_titles: List of titles corresponding to images
        """
        num_images = len(steps_images)
        rows = 2
        cols = math.ceil(num_images / rows)

        for r in range(rows):
            columns = st.columns(cols)
            for c in range(cols):
                idx = r * cols + c
                if idx < num_images:
                    with columns[c]:
                        st.subheader(steps_titles[idx])
                        st.image(steps_images[idx], width=200)
    
    @classmethod
    def enhance_prescription(cls, image_pil, return_steps=False):
        """
        Apply full image enhancement pipeline to prescription image.
        
        Args:
            image_pil: PIL Image object of the prescription
            return_steps: If True, return intermediate processing steps
            
        Returns:
            Enhanced image and optionally processing steps
        """
        # Convert PIL to OpenCV format
        image_np = np.array(image_pil)
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            original_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        else:
            original_cv = image_np.copy()
            
        # Store processing steps if requested
        steps_images = []
        steps_titles = []
        
        # Keep original for display
        original_rgb = cv2.cvtColor(original_cv, cv2.COLOR_BGR2RGB) if len(image_np.shape) == 3 else original_cv
        if return_steps:
            steps_images.append(original_rgb)
            steps_titles.append("Original Image")
            
        # Step 1: Resize image if needed
        resized = cls.resize_image(original_cv)
        if return_steps:
            resized_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB) if len(resized.shape) == 3 else resized
            steps_images.append(resized_rgb)
            steps_titles.append("Resized Image")
            
        # Step 2: Convert to grayscale
        gray = cls.convert_to_grayscale(resized)
        if return_steps:
            steps_images.append(gray)
            steps_titles.append("Grayscale Conversion")
            
        # Step 3: Apply adaptive thresholding
        threshold = cls.apply_adaptive_threshold(gray)
        if return_steps:
            steps_images.append(threshold)
            steps_titles.append("Adaptive Thresholding")
            
        # Step 4: Apply noise reduction
        denoised = cls.reduce_noise(threshold)
        if return_steps:
            steps_images.append(denoised)
            steps_titles.append("Noise Reduction")
            
        # Step 5: Enhance edges
        sharpened = cls.enhance_edges(denoised)
        if return_steps:
            steps_images.append(sharpened)
            steps_titles.append("Edge Enhancement")
            
        # Step 6: Enhance contrast
        contrast_enhanced = cls.enhance_contrast(sharpened)
        if return_steps:
            steps_images.append(np.array(contrast_enhanced))
            steps_titles.append("Contrast Enhancement (Final)")
            
        # Return results
        if return_steps:
            return contrast_enhanced, steps_images, steps_titles
        else:
            return contrast_enhanced
