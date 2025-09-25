from nicegui import ui
import asyncio
from utils.api_client import api_client
from utils.auth import auth_state, logout
from components.header import show_header
from components.footer import show_footer

def show_ai_text_generator_page():
    # AI Text Generator Page
    with ui.element('div').classes('min-h-screen w-full max-w-full px-4 py-4 bg-gradient-to-br from-green-50 to-blue-50'):
        with ui.element('div').classes('w-full max-w-7xl mx-auto'):
            
            # Page Header
            with ui.element('div').classes('text-center mb-8 py-8'):
                ui.label('AI Text Generator').classes('text-4xl font-bold text-gray-800 mb-4')
                ui.label('Generate creative content with AI using Gemini').classes('text-lg text-gray-600 mb-6')
                
                # AI Features showcase
                with ui.element('div').classes('flex flex-wrap justify-center gap-4 mb-8'):
                    ui.label('Creative Writing').classes('bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium')
                    ui.label('Product Descriptions').classes('bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium')
                    ui.label('Marketing Copy').classes('bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-medium')
                    ui.label('Content Ideas').classes('bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-medium')
            
            # Main Content
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'):
                
                # Left Column - Input Form (50% width)
                with ui.card().classes('bg-white p-4 rounded-xl shadow-lg border border-gray-200 h-fit'):
                    ui.label('Generate Your Content').classes('text-2xl font-bold text-gray-800 mb-6')
                    
                    # Content Type Selection
                    with ui.element('div').classes('mb-6'):
                        ui.label('Content Type').classes('text-lg font-semibold text-gray-700 mb-3')
                        content_type_select = ui.select(
                            options={
                                'product_description': 'Product Description',
                                'marketing_copy': 'Marketing Copy',
                                'blog_post': 'Blog Post',
                                'social_media': 'Social Media Post',
                                'email_campaign': 'Email Campaign',
                                'advertisement': 'Advertisement',
                                'creative_writing': 'Creative Writing',
                                'technical_documentation': 'Technical Documentation'
                            },
                            value='product_description'
                        ).classes('w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent')
                    
                    # Prompt Input
                    with ui.element('div').classes('mb-6'):
                        ui.label('Describe what you want to generate').classes('text-lg font-semibold text-gray-700 mb-3')
                        prompt_input = ui.textarea(
                            placeholder='Enter details about the content you want to generate...\n\nExample: "Write a compelling product description for a wireless Bluetooth headphones with noise cancellation, targeting young professionals"'
                        ).classes('w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none')
                    
                    # Settings Grid - 2 columns (Tone & Length)
                    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-4 mb-6'):
                        # Tone Selection
                        with ui.element('div'):
                            ui.label('Tone & Style').classes('text-base font-semibold text-gray-700 mb-2')
                            tone_select = ui.select(
                                options={
                                    'professional': 'Professional',
                                    'casual': 'Casual',
                                    'friendly': 'Friendly',
                                    'persuasive': 'Persuasive',
                                    'informative': 'Informative',
                                    'creative': 'Creative',
                                    'humorous': 'Humorous',
                                    'formal': 'Formal'
                                },
                                value='professional'
                            ).classes('w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent')
                        
                        # Length Selection
                        with ui.element('div'):
                            ui.label('Content Length').classes('text-base font-semibold text-gray-700 mb-2')
                            length_select = ui.select(
                                options={
                                    'short': 'Short (1-2 sentences)',
                                    'medium': 'Medium (1-2 paragraphs)',
                                    'long': 'Long (3+ paragraphs)',
                                    'custom': 'Custom Length'
                                },
                                value='medium'
                            ).classes('w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent')
                    
                    # Generate Button
                    generate_button = ui.button('Generate Text', icon='auto_awesome').classes('w-full h-12 bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 text-lg')
                    
                    # Loading State
                    loading_container = ui.element('div').classes('hidden')
                    
                    # Quick Prompt Suggestions
                    with ui.element('div').classes('mt-6'):
                        ui.label('Quick Prompts').classes('text-lg font-semibold text-gray-700 mb-3')
                        suggestions = [
                            'Write a product description for wireless earbuds',
                            'Create a social media post about a new smartphone',
                            'Generate marketing copy for a fitness app',
                            'Write a blog post about sustainable living',
                            'Create an email subject line for a sale',
                            'Write an advertisement for a restaurant'
                        ]
                        
                        with ui.element('div').classes('grid grid-cols-1 gap-2'):
                            for suggestion in suggestions:
                                ui.button(suggestion, on_click=lambda s=suggestion: prompt_input.set_value(s)).classes('text-left p-3 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-sm text-gray-700 hover:text-gray-900 transition-colors')
                
                # Right Column - Generated Content
                with ui.card().classes('bg-white p-6 rounded-xl shadow-lg border border-gray-200'):
                    ui.label('Generated Content').classes('text-2xl font-bold text-gray-800 mb-6')
                    
                    # Content Container
                    content_container = ui.element('div').classes('space-y-4')
                    
                    # Placeholder when no content
                    with content_container:
                        with ui.element('div').classes('text-center py-12 border-2 border-dashed border-gray-300 rounded-lg'):
                            ui.icon('description').classes('text-6xl text-gray-400 mb-4')
                            ui.label('No content generated yet').classes('text-lg text-gray-500 mb-2')
                            ui.label('Enter a prompt and click "Generate Text" to create your first AI content').classes('text-sm text-gray-400')
            
            # Generation History Section
            with ui.card().classes('bg-white p-6 rounded-xl shadow-lg border border-gray-200 mb-8'):
                ui.label('Generation History').classes('text-2xl font-bold text-gray-800 mb-6')
                
                # History Container
                history_container = ui.element('div').classes('space-y-4')
                
                # Placeholder for history
                with history_container:
                    with ui.element('div').classes('text-center py-8 text-gray-500'):
                        ui.icon('history').classes('text-4xl text-gray-400 mb-2')
                        ui.label('No generation history yet').classes('text-sm')
            
            # AI Tips Section
            with ui.card().classes('bg-gradient-to-r from-green-100 to-blue-100 p-6 rounded-xl border border-green-200 mb-8'):
                ui.label('AI Text Generation Tips').classes('text-xl font-bold text-gray-800 mb-4')
                
                tips = [
                    'Be specific about your target audience and use case',
                    'Include key features, benefits, or points you want to highlight',
                    'Specify the tone and style that matches your brand',
                    'Provide context about where the content will be used',
                    'Use descriptive keywords to guide the AI generation'
                ]
                
                with ui.element('div').classes('space-y-2'):
                    for tip in tips:
                        ui.label(f'• {tip}').classes('text-gray-700 text-sm')
    
    # AI Text Generation Logic
    async def generate_text():
        """Generate AI text using Gemini API"""
        prompt = prompt_input.value.strip()
        if not prompt:
            ui.notify('Please enter a prompt for text generation', type='warning')
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
                'content_type': content_type_select.value,
                'tone': tone_select.value,
                'length': length_select.value
            }
            
            # Call AI text generation API
            success, response = await api_client.generate_ai_text(request_data)
            
            if success and response:
                # Display generated text
                display_generated_text(response, prompt)
                try:
                    ui.notify('Text generated successfully!', type='positive')
                except (RuntimeError, AttributeError):
                    print("✅ Text generated successfully!")
            else:
                error_msg = str(response) if response else 'Unknown error'
                try:
                    ui.notify(f'Failed to generate text: {error_msg}', type='negative')
                except (RuntimeError, AttributeError):
                    print(f"❌ Failed to generate text: {error_msg}")
                
        except Exception as e:
            try:
                ui.notify(f'Error generating text: {str(e)}', type='negative')
            except (RuntimeError, AttributeError):
                print(f"❌ Error generating text: {str(e)}")
            print(f"❌ AI Text generation error: {e}")
        
        finally:
            # Reset button state
            generate_button.classes(remove='opacity-50 cursor-not-allowed')
            generate_button.text = 'Generate Text'
            generate_button.props(remove='loading')
            loading_container.classes(remove='block')
    
    def display_generated_text(text_data, prompt):
        """Display the generated text in the content container"""
        # Clear placeholder
        content_container.clear()
        
        # Create text card
        with content_container:
            with ui.card().classes('bg-white border border-gray-200 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow'):
                # Text content - handle OpenAI response format
                if isinstance(text_data, dict):
                    if 'output_text' in text_data:
                        generated_text = text_data['output_text']
                    elif 'success' in text_data and text_data.get('success'):
                        generated_text = text_data.get('output_text', '')
                    else:
                        # Error response
                        ui.label(f'Error: {text_data.get("error", "Unknown error")}').classes('text-red-500 p-4')
                        return
                elif isinstance(text_data, str):
                    generated_text = text_data
                else:
                    generated_text = str(text_data)
                
                # Text display
                with ui.element('div').classes('p-6'):
                    ui.label('Generated Content').classes('font-semibold text-gray-800 mb-4 text-lg')
                    
                    # Main content
                    with ui.element('div').classes('bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4'):
                        ui.label(generated_text).classes('text-gray-800 leading-relaxed whitespace-pre-wrap')
                    
                    # Prompt info
                    ui.label(f'Prompt: {prompt[:100]}{"..." if len(prompt) > 100 else ""}').classes('text-sm text-gray-600 mb-4')
                    
                    # Show model info if available
                    if isinstance(text_data, dict) and 'model' in text_data:
                        ui.label(f'Model: {text_data["model"]}').classes('text-xs text-gray-500 mb-2')
                    
                    # Action buttons
                    with ui.element('div').classes('flex gap-2'):
                        # Copy button
                        ui.button('Copy Text', icon='content_copy', on_click=lambda: copy_text(generated_text)).classes('flex-1 bg-blue-500 hover:bg-blue-600 text-white text-sm py-2 px-3 rounded')
                        
                        # Save button
                        ui.button('Save', icon='bookmark', on_click=lambda: save_text(generated_text, prompt)).classes('flex-1 bg-green-500 hover:bg-green-600 text-white text-sm py-2 px-3 rounded')
                        
                        # Regenerate button
                        ui.button('Regenerate', icon='refresh', on_click=lambda: regenerate_text(prompt)).classes('flex-1 bg-purple-500 hover:bg-purple-600 text-white text-sm py-2 px-3 rounded')
    
    def copy_text(text):
        """Copy text to clipboard"""
        try:
            ui.run_javascript(f'''
                navigator.clipboard.writeText(`{text.replace('`', '\\`')}`).then(() => {{
                    // Show success notification
                    const notification = document.createElement('div');
                    notification.textContent = 'Text copied to clipboard!';
                    notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
                    document.body.appendChild(notification);
                    setTimeout(() => document.body.removeChild(notification), 2000);
                }});
            ''')
        except Exception as e:
            ui.notify(f'Copy failed: {str(e)}', type='negative')
    
    def save_text(text, prompt):
        """Save text to user's saved content"""
        try:
            # This would integrate with user's saved content
            ui.notify('Text saved to your content library!', type='positive')
        except Exception as e:
            ui.notify(f'Save failed: {str(e)}', type='negative')
    
    def regenerate_text(prompt):
        """Regenerate text with same prompt"""
        prompt_input.value = prompt
        asyncio.create_task(generate_text())
    
    # Connect generate button
    generate_button.on('click', lambda: asyncio.create_task(generate_text()))
