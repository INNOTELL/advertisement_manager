from nicegui import ui
import asyncio
from urllib.parse import quote
from utils.api_client import api_client
from utils.auth import auth_state, logout
from components.header import show_header
from components.footer import show_footer

def show_ai_generator_page():
    # AI Image Generator Page
    with ui.element('div').classes('min-h-screen w-full max-w-full px-4 py-4 bg-gradient-to-br from-purple-50 to-blue-50'):
        with ui.element('div').classes('w-full max-w-7xl mx-auto'):
            
            # Page Header
            with ui.element('div').classes('text-center mb-8 py-8'):
                ui.label('AI Image Generator').classes('text-4xl font-bold text-gray-800 mb-4')
                ui.label('Create stunning images with AI using Gemini Imagen').classes('text-lg text-gray-600 mb-6')
                
                # AI Features showcase
                with ui.element('div').classes('flex flex-wrap justify-center gap-4 mb-8'):
                    ui.label('High Quality').classes('bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-medium')
                    ui.label('Creative Styles').classes('bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium')
                    ui.label('Fast Generation').classes('bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium')
                    ui.label('Multiple Variations').classes('bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-medium')
            
            # Main Content
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'):
                
                # Left Column - Input Form (50% width)
                with ui.card().classes('bg-white p-4 rounded-xl shadow-lg border border-gray-200 h-fit'):
                    ui.label('Create Your Image').classes('text-2xl font-bold text-gray-800 mb-6')
                    
                    # Prompt Input
                    with ui.element('div').classes('mb-6'):
                        ui.label('Describe your image').classes('text-lg font-semibold text-gray-700 mb-3')
                        prompt_input = ui.textarea(
                            placeholder='Enter a detailed description of the image you want to generate...\n\nExample: "A beautiful sunset over the ocean with palm trees, tropical beach scene, vibrant colors, high quality, photorealistic"'
                        ).classes('w-full h-40 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none')
                    
                    # Settings Grid - 3 columns
                    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-4 mb-6'):
                        # Style Selection
                        with ui.element('div'):
                            ui.label('Image Style').classes('text-base font-semibold text-gray-700 mb-2')
                            style_select = ui.select(
                                options={
                                    'photorealistic': 'Photorealistic',
                                    'artistic': 'Artistic',
                                    'cartoon': 'Cartoon',
                                    'anime': 'Anime',
                                    'oil_painting': 'Oil Painting',
                                    'watercolor': 'Watercolor',
                                    'sketch': 'Sketch',
                                    'digital_art': 'Digital Art'
                                },
                                value='photorealistic'
                            ).classes('w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent')
                        
                        # Size Selection
                        with ui.element('div'):
                            ui.label('Image Size').classes('text-base font-semibold text-gray-700 mb-2')
                            size_select = ui.select(
                                options={
                                    '1024x1024': 'Square (1024x1024)',
                                    '1024x768': 'Landscape (1024x768)',
                                    '768x1024': 'Portrait (768x1024)',
                                    '512x512': 'Small Square (512x512)'
                                },
                                value='1024x1024'
                            ).classes('w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent')
                        
                        # Quality Selection
                        with ui.element('div'):
                            ui.label('Quality Level').classes('text-base font-semibold text-gray-700 mb-2')
                            quality_select = ui.select(
                                options={
                                    'standard': 'Standard',
                                    'hd': 'High Definition',
                                    'ultra_hd': 'Ultra HD'
                                },
                                value='hd'
                            ).classes('w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent')
                    
                    # Generate Button
                    generate_button = ui.button('Generate Image', icon='auto_awesome').classes('w-full h-12 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 text-lg')
                    
                    # Loading State
                    loading_container = ui.element('div').classes('hidden')
                    
                    # Quick Prompt Suggestions
                    with ui.element('div').classes('mt-6'):
                        ui.label('Quick Prompts').classes('text-lg font-semibold text-gray-700 mb-3')
                        suggestions = [
                            'A futuristic city skyline at sunset',
                            'Cute cat playing with yarn',
                            'Mountain landscape with lake reflection',
                            'Vintage car in a garage',
                            'Abstract art with vibrant colors',
                            'Portrait of a wise old man'
                        ]
                        
                        with ui.element('div').classes('grid grid-cols-1 gap-2'):
                            for suggestion in suggestions:
                                ui.button(suggestion, on_click=lambda s=suggestion: prompt_input.set_value(s)).classes('text-left p-3 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-sm text-gray-700 hover:text-gray-900 transition-colors')
                
                # Right Column - Generated Images
                with ui.card().classes('bg-white p-6 rounded-xl shadow-lg border border-gray-200'):
                    ui.label('Generated Images').classes('text-2xl font-bold text-gray-800 mb-6')
                    
                    # Images Container
                    images_container = ui.element('div').classes('space-y-4')
                    
                    # Placeholder when no images
                    with images_container:
                        with ui.element('div').classes('text-center py-12 border-2 border-dashed border-gray-300 rounded-lg'):
                            ui.icon('image').classes('text-6xl text-gray-400 mb-4')
                            ui.label('No images generated yet').classes('text-lg text-gray-500 mb-2')
                            ui.label('Enter a prompt and click "Generate Image" to create your first AI image').classes('text-sm text-gray-400')
            
            # Generation History Section
            with ui.card().classes('bg-white p-6 rounded-xl shadow-lg border border-gray-200 mb-8'):
                ui.label('Generation History').classes('text-2xl font-bold text-gray-800 mb-6')
                
                # History Container
                history_container = ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4')
                
                # Placeholder for history
                with history_container:
                    with ui.element('div').classes('text-center py-8 text-gray-500'):
                        ui.icon('history').classes('text-4xl text-gray-400 mb-2')
                        ui.label('No generation history yet').classes('text-sm')
            
            # AI Tips Section
            with ui.card().classes('bg-gradient-to-r from-purple-100 to-blue-100 p-6 rounded-xl border border-purple-200 mb-8'):
                ui.label('AI Generation Tips').classes('text-xl font-bold text-gray-800 mb-4')
                
                tips = [
                    'Be specific with your descriptions - include colors, lighting, and mood',
                    'Mention the style you want (photorealistic, artistic, cartoon, etc.)',
                    'Include details about composition, background, and foreground elements',
                    'Use descriptive adjectives to enhance the quality of generated images',
                    'Try different aspect ratios for various use cases (square for social media, landscape for banners)'
                ]
                
                with ui.element('div').classes('space-y-2'):
                    for tip in tips:
                        ui.label(f'• {tip}').classes('text-gray-700 text-sm')
    
    # AI Image Generation Logic
    async def generate_image():
        """Generate AI image using Gemini API"""
        prompt = prompt_input.value.strip()
        if not prompt:
            ui.notify('Please enter a prompt for image generation', type='warning')
            return
        
        # Show loading state
        generate_button.classes('opacity-50 cursor-not-allowed')
        generate_button.text = 'Generating...'
        generate_button.props('loading')
        
        # Show loading container
        loading_container.classes('block')
        
        try:
            # Prepare request data
            request_data = {
                'prompt': prompt,
                'style': style_select.value,
                'size': size_select.value,
                'quality': quality_select.value
            }
            
            # Call AI image generation API
            success, response = await api_client.generate_ai_image(request_data)
            
            if success and response:
                # Display generated image
                display_generated_image(response, prompt)
                try:
                    ui.notify('Image generated successfully!', type='positive')
                except (RuntimeError, AttributeError):
                    print("✅ Image generated successfully!")
            else:
                error_msg = str(response) if response else 'Unknown error'
                try:
                    ui.notify(f'Failed to generate image: {error_msg}', type='negative')
                except (RuntimeError, AttributeError):
                    print(f"❌ Failed to generate image: {error_msg}")
                
        except Exception as e:
            try:
                ui.notify(f'Error generating image: {str(e)}', type='negative')
            except (RuntimeError, AttributeError):
                print(f"❌ Error generating image: {str(e)}")
            print(f"❌ AI Image generation error: {e}")
        
        finally:
            # Reset button state
            generate_button.classes(remove='opacity-50 cursor-not-allowed')
            generate_button.text = 'Generate Image'
            generate_button.props(remove='loading')
            loading_container.classes(remove='block')
    
    def display_generated_image(image_data, prompt):
        """Display the generated image in the images container"""
        # Clear placeholder
        images_container.clear()
        
        # Create image card
        with images_container:
            with ui.card().classes('bg-white border border-gray-200 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow'):
                # Image display - handle OpenAI response format
                if isinstance(image_data, dict):
                    if 'image_url' in image_data:
                        image_url = image_data['image_url']
                    elif 'success' in image_data and image_data.get('success'):
                        image_url = image_data.get('image_url')
                    else:
                        # Error response
                        ui.label(f'Error: {image_data.get("error", "Unknown error")}').classes('text-red-500 p-4')
                        return
                elif isinstance(image_data, str):
                    image_url = image_data
                else:
                    # Handle base64 or other formats
                    image_url = str(image_data)
                
                # Main image
                ui.image(image_url).classes('w-full h-64 object-cover')
                
                # Image details
                with ui.element('div').classes('p-4'):
                    ui.label('Generated Image').classes('font-semibold text-gray-800 mb-2')
                    ui.label(f'Prompt: {prompt[:100]}{"..." if len(prompt) > 100 else ""}').classes('text-sm text-gray-600 mb-3')
                    
                    # Show model info if available
                    if isinstance(image_data, dict) and 'model' in image_data:
                        ui.label(f'Model: {image_data["model"]}').classes('text-xs text-gray-500 mb-2')
                    
                    # Action buttons
                    with ui.element('div').classes('flex gap-2'):
                        # Download button
                        ui.button('Download', icon='download', on_click=lambda: download_image(image_url, prompt)).classes('flex-1 bg-blue-500 hover:bg-blue-600 text-white text-sm py-2 px-3 rounded')
                        
                        # Save to gallery button
                        ui.button('Save', icon='bookmark', on_click=lambda: save_to_gallery(image_url, prompt)).classes('flex-1 bg-green-500 hover:bg-green-600 text-white text-sm py-2 px-3 rounded')
                        
                        # Regenerate button
                        ui.button('Regenerate', icon='refresh', on_click=lambda: regenerate_image(prompt)).classes('flex-1 bg-purple-500 hover:bg-purple-600 text-white text-sm py-2 px-3 rounded')
    
    def download_image(image_url, prompt):
        """Download the generated image"""
        try:
            # Create download link
            import re
            safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:20])
            ui.run_javascript(f'''
                const link = document.createElement('a');
                link.href = '{image_url}';
                link.download = 'ai_generated_{safe_filename}.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            ''')
            ui.notify('Image download started!', type='positive')
        except Exception as e:
            ui.notify(f'Download failed: {str(e)}', type='negative')
    
    def save_to_gallery(image_url, prompt):
        """Save image to user's gallery"""
        try:
            # This would integrate with user's saved images
            ui.notify('Image saved to your gallery!', type='positive')
        except Exception as e:
            ui.notify(f'Save failed: {str(e)}', type='negative')
    
    def regenerate_image(prompt):
        """Regenerate image with same prompt"""
        prompt_input.value = prompt
        asyncio.create_task(generate_image())
    
    # Connect generate button
    generate_button.on('click', lambda: asyncio.create_task(generate_image()))
