"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

import json, requests

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class ConceptXBlock(XBlock):
    """
    This XBlock allows concept tagging in a course. 
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    server = String(
           scope = Scope.settings, 
           help = "Concept map server URL"
        )

    concept_map = String(
        scope  = Scope.user_state_summary, # User scope: Global. Block scope: Usage
        help = "Concept map"
        )

    @XBlock.json_handler
    def update_concept_map(self, request, suffix):
        print request
        self.concept_map = json.dumps(request)
        print "Wrote:", self.concept_map
        return {'success':True}

    @XBlock.json_handler
    def relay_handler(self, request, suffix):
        #print request, type(request), dict(request)
        url = self.server+request['suffix']
        r = requests.get(url, params=request) 
        #print url,":", r.text[:80]
        return json.loads(r.text)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ConceptXBlock, shown to students
        when viewing courses.
        """
        print "HERE", self.concept_map
        html = self.resource_string("static/html/concept.html")#.replace("PLACEHOLDER_FOR_CONCEPT_MAP",json.dumps(self.concept_map))
        #print self.server
        #print html.format
        cm = self.concept_map
        print "Read", cm
        frag = Fragment(html.replace("PLACEHOLDER_FOR_CONCEPT_MAP",cm).replace("SERVER", self.server))   #)#format(server = self.server, concept_map = cm))
        frag.add_css_url("https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css")
        frag.add_css(self.resource_string("static/css/concept.css"))

        frag.add_javascript_url("http://builds.handlebarsjs.com.s3.amazonaws.com/handlebars-v1.3.0.js")
#        frag.add_javascript_url("https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js")
        frag.add_javascript_url("https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js")

        frag.add_javascript(self.resource_string("static/js/concept.js"))

        frag.initialize_js('ConceptXBlock')
        print self.xml_text_content()
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ConceptXBlock",
             """<vertical_demo>
                  <Concept server="http://pmitros.edx.org:8000/"> </Concept>
                </vertical_demo>
             """),
        ]
