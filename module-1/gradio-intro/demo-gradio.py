import gradio as gr



def my_function(input):
    # process input
    return input

demo = gr.Interface(fn=my_function, inputs="text", outputs="text")
demo.launch()





# ===========================================================================

# def greet(name):
#     return 'Hello ' + name

# demo = gr.Interface(
#     fn = greet,
#     inputs = gr.Textbox(label="Enter name"),
#     outputs=gr.Textbox(label="Greeting")
# )

# # demo.launch()
# demo.launch(share = True)