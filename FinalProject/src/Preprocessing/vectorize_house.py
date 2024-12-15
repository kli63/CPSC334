import os
from pathlib import Path
import shutil
import json
from datetime import datetime
from linedraw import vectorize, makesvg  # Import the specific functions we need

class ComponentVectorizer:
    def __init__(self):
        # Define paths relative to project root
        self.PROJECT_ROOT = Path(__file__).parent.parent.parent
        self.INPUT_BASE_DIR = self.PROJECT_ROOT / "assets" / "images" / "components"
        self.OUTPUT_BASE_DIR = self.PROJECT_ROOT / "assets" / "data" / "components"

        # Define COMPONENTS
        self.COMPONENTS = ['middle', 'top_left', 'top_right', 'signature']

        # Initialize counters for statistics
        self.total_lines_count = 0
        self.total_segments_count = 0
        self.total_images_processed = 0

        # Parameters for vectorize (for logging)
        self.resolution = 1024
        self.draw_contours = 4
        self.repeat_contours = 1
        self.draw_hatch = False
        self.repeat_hatch = 0

    def setup_directories(self):
        """Create output directory structure for each component directory without clearing everything."""

        # Make sure the base output directory exists
        self.OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)

        # For each component, remove and recreate its json and svg subdirectories
        for quadrant in self.COMPONENTS:
            json_dir = self.OUTPUT_BASE_DIR / quadrant / "json"
            svg_dir = self.OUTPUT_BASE_DIR / quadrant / "svg"
            
            # Remove existing json and svg directories if they exist
            if json_dir.exists():
                shutil.rmtree(json_dir)
            if svg_dir.exists():
                shutil.rmtree(svg_dir)
            
            # Recreate them
            json_dir.mkdir(parents=True, exist_ok=True)
            svg_dir.mkdir(parents=True, exist_ok=True)

    def process_components(self):
        """Process all components in each quadrant directory."""
        self.setup_directories()
        
        for quadrant in self.COMPONENTS:
            input_dir = self.INPUT_BASE_DIR / quadrant
            
            if not input_dir.exists():
                print(f"Warning: Input directory {input_dir} does not exist!")
                continue
                
            print(f"\nProcessing components in {quadrant}...")
            
            # Get all image files in the quadrant directory
            image_files = [f for f in input_dir.glob("*") if f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.bmp')]
            
            if not image_files:
                print(f"No images found in {input_dir}")
                continue
            
            for image_file in image_files:
                print(f"Vectorizing {image_file.name}...")
                
                try:
                    # Vectorize parameters
                    lines = vectorize(
                        str(image_file),
                        resolution=self.resolution,
                        draw_contours=self.draw_contours,
                        repeat_contours=self.repeat_contours,
                        draw_hatch=self.draw_hatch,
                        repeat_hatch=self.repeat_hatch
                    )
                    
                    if not lines:
                        print(f"  No lines generated for {image_file.name}")
                        continue

                    # Save SVG
                    svg_path = self.OUTPUT_BASE_DIR / quadrant / "svg" / f"{image_file.stem}.svg"
                    with open(svg_path, 'w') as f:
                        f.write(makesvg(lines))

                    # Save JSON
                    json_path = self.OUTPUT_BASE_DIR / quadrant / "json" / f"{image_file.stem}.json"
                    with open(json_path, 'w') as f:
                        json.dump(lines, f, indent=4)
                        
                    # Update counters
                    self.total_images_processed += 1
                    self.total_lines_count += len(lines)
                    segments = sum((len(line)-1 for line in lines))
                    self.total_segments_count += segments
                    
                    print(f"  Successfully processed {image_file.name}")
                    
                except Exception as e:
                    print(f"  Error processing {image_file.name}: {str(e)}")

    def log_stats(self):
        """Log the average lines and segments along with parameters to a text file."""
        if self.total_images_processed > 0:
            avg_lines = self.total_lines_count / self.total_images_processed
            avg_segments = self.total_segments_count / self.total_images_processed
        else:
            avg_lines = 0
            avg_segments = 0
        
        log_path = self.OUTPUT_BASE_DIR / "vectorization_stats.txt"
        with open(log_path, 'a') as f:
            f.write(
                f"{datetime.now().isoformat()} - "
                f"Params: resolution={self.resolution}, draw_contours={self.draw_contours}, "
                f"repeat_contours={self.repeat_contours}, draw_hatch={self.draw_hatch}, "
                f"repeat_hatch={self.repeat_hatch} | "
                f"Average Lines: {avg_lines:.2f}, Average Segments: {avg_segments:.2f}\n"
            )
        print(f"Appended stats to {log_path}")


def main():
    vectorizer = ComponentVectorizer()
    vectorizer.process_components()
    vectorizer.log_stats()
    print("\nVectorization complete!")

if __name__ == "__main__":
    main()
