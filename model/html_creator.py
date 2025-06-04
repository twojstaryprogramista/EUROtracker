from utils.names import ModelValues, MapValues

class HTMLCreator:
    def __init__(self):
        self.save_path = ModelValues.MAP_DIR.value
        self.html_edit =MapValues.HTML_EDIT.value

    def save(self,fig):
        html_content = self.__editHTML(fig)
        self.__save(html_content)


    def set_save_path(self,save_path):
        self.save_path=save_path
    def set_html_edit(self,html_edit):
        self.html_edit=html_edit

    def __editHTML(self,fig):
        html_content = fig.to_html(
        full_html=True,
        #include_plotlyjs='cdn', 
        config={'displayModeBar': False}
        )

        html_content = html_content.replace(
            "<head>",
            self.html_edit
        )
        return html_content

    def __save(self,html_content):
        with open(self.save_path, "w", encoding="utf-8") as f:
            f.write(html_content)