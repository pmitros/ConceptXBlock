"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class XonceptXBlock(XBlock):
    """
    This XBlock will play an MP3 file as an HTML5 Xoncept element. 
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    src = String(
           scope = Scope.settings, 
           help = "URL for MP3 file to play"
        )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the XonceptXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/xoncept.html")
        print self.src
        print html.format
        frag = Fragment(html.format(src = self.src))
        frag.add_css_url("https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css")
        frag.add_css(self.resource_string("static/css/xoncept.css"))

        frag.add_javascript_url("http://builds.handlebarsjs.com.s3.amazonaws.com/handlebars-v1.3.0.js")
#        frag.add_javascript_url("https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js")
        frag.add_javascript_url("https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js")

        frag.add_javascript(self.resource_string("static/js/xoncept.js"))

        #frag.initialize_js('XonceptXBlock')
        print self.xml_text_content()
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("XonceptXBlock",
             """<vertical_demo>
                  <Xoncept src="http://localhost/Ikea.mp3"> </Xoncept>
                </vertical_demo>
             """),
        ]
