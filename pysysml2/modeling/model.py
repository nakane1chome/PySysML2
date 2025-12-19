import os
from pathlib import Path

from anytree import RenderTree, NodeMixin
from anytree.exporter import DotExporter, JsonExporter
import antlr4
import pandas as pd

from pysysml2.modeling.element import (
    Attribute,
    Comment,
    Connection,
    ConnectionEndPart,
    Doc,
    Element,
    EnumDef,
    EnumValue,
    Import,
    Include,
    Item,
    Objective,
    Package,
    Part,
    Port,
    UseCase,
    Relationship,
    RelationshipConnect,
    RelationshipRedefines,
    RelationshipSpecializes,
    RelationshipMessage
)
from pysysml2.grammar import sysml2_model_visitor as smv
from pysysml2.grammar.distpy.SysML2Lexer import SysML2Lexer
from pysysml2.grammar.distpy.SysML2Parser import SysML2Parser


# Module constants
# ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
NODE_ROOT_NAME = "root"


class Model(NodeMixin):
    """_summary_"""

    def __init__(self):
        """_summary_"""

        super(Model, self).__init__()
        self.name = NODE_ROOT_NAME
        self.input_file = None
        self.sysml2_visitor = None

    def from_sysml2_file(self, file):
        """_summary_
        This function is used to read in a SysML2 file and create a model.
        TODO: Consider integrating this with the antlr4 visitor. The only reason
        why this is separate is to keep antlr4 code abstracted from the rest of
        PySysML2. For now, I import antlr4 into this, but antlr4 related code
        doesn't import PySysML2. The main drawback I see is that the parse
        loop is essentially executed twice-- but readibility makes it worth it.
        Args:
            file (_type_): _description_

        Raises:
            NotImplementedError: _description_
            NotImplementedError: _description_
            NotImplementedError: _description_
            Exception: _description_

        Returns:
            _type_: _description_
        """
        # Read in the file
        self.input_file = file
        input = antlr4.FileStream(self.input_file)
        # Create the lexer and parser
        # Note, this is all Antler4 generated code
        lexer = SysML2Lexer(input)
        commonTokenStream = antlr4.CommonTokenStream(lexer)
        sysml2Parser = SysML2Parser(commonTokenStream)
        tree = sysml2Parser.model()
        # Create the visitor class. This is a custom class that extends the
        # Antler4 generated visitor class with SysML2 specific functionality
        self.sysml2_visitor = smv.ModelTreeSysML2Visitor()
        modelCtx = self.sysml2_visitor.visit(tree) # Run visitor
        # This is a dictionary of all the elements in the model, created by the
        # visitor. This serves as the basis for creating the model tree
        model_table_dict = self.sysml2_visitor.model_table_dict
        # Each value is keyed by the idx of the element. The value is a
        # dictionary of the element's attributes. The value also contains the
        # idx of the parent element

        for (k, v) in model_table_dict.items():

            # Create the parent node. It the root node if it doesn't have a
            # parent node.
            v["parent"] = (
                self
                if v["idx_parent"] is None
                else self.find_element_by_idx(v["idx_parent"])
            )

            # This case statement is used to create the correct type of element
            # based on the sysml2_type attribute of the element. When a new 
            # element is constructed, it is added to the model tree as a child
            # of its parent node.Note that the dictionary of attributes for each
            # element are the constructor arguments for the Element class.
            if smv._SML2_KWS.KW_CONNECT.value in v["keywords"]:
                RelationshipConnect(**v)
            elif smv._SML2_KWS.KW_SPECIALIZES.value in v["keywords"]:
                RelationshipSpecializes(**v)
            elif smv._SML2_KWS.KW_REDEFINES.value in v["keywords"]:
                RelationshipRedefines(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_MESSAGE.value:
                RelationshipMessage(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_ABOUT.value:
                raise NotImplementedError(
                    "{} keyword not implemented".format(smv._SML2_KWS.KW_ABOUT.value)
                )
            elif v["sysml2_type"] == smv._SML2_KWS.KW_ACTOR.value:
                raise NotImplementedError(
                    "{} keyword not implemented".format(smv._SML2_KWS.KW_ACTOR.value)
                )
            elif v["sysml2_type"] == smv._SML2_KWS.KW_ATTRIBUTE.value:
                Attribute(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_COMMENT.value:
                Comment(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_CONNECTION.value:
                Connection(**v)
            elif v["sysml2_type"] == "{}{}".format(smv._SML2_KWS.KW_END.value, smv._SML2_KWS.KW_PART.value):
                ConnectionEndPart(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_DOC.value:
                Doc(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_IMPORT.value:
                Import(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_ITEM.value:
                Item(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_OBJECTIVE.value:
                Objective(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_PACKAGE.value:
                Package(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_PART.value:
                Part(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_PORT.value:
                Port(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_INCLUDE.value:
                Include(**v)
            elif v["sysml2_type"] == "{}{}".format(
                smv._SML2_KWS.KW_USE.value, smv._SML2_KWS.KW_CASE.value
            ):
                UseCase(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_ENUM.value:
                EnumDef(**v)
            elif v["sysml2_type"] == "enum_value":
                EnumValue(**v)
            elif v["sysml2_type"] == smv._SML2_KWS.KW_ABOUT.value:
                raise NotImplementedError(
                    "{} keyword not implemented".format(smv._SML2_KWS.KW_ABOUT.value)
                )
            else:
                raise Exception("Unknown root sysml2 type: {}".format(v["sysml2_type"]))

        return self

    def find_element_by_idx(self, idx: int):
        """_summary_

        Args:
            idx (int): _description_
        """
        # Find the node that has the idx
        for pre, fill, node in RenderTree(self):
            if isinstance(node, Model):
                continue
            if getattr(node, "idx") == idx:
                return node
        return None

    def to_excel(self, out_dir=None, file=None):
        """_summary_

        Args:
            out_dir (_type_, optional): _description_. Defaults to None.
            file (_type_, optional): _description_. Defaults to None.
        """
        out_file = self._out_file_handler(".xlsx", out_dir, file)
        dd = self.to_dict()
        df = pd.DataFrame.from_dict(dd, orient="index")
        df.to_excel(out_file, index=False)

    def to_csv(self, out_dir=None, file=None):
        """_summary_

        Args:
            out_dir (_type_): _description_
        """
        # Create the output directory if it doesn't exist, set file name
        out_file = self._out_file_handler(".csv", out_dir, file)
        # Write to CSV from the pandas dataframe
        df = self.sysml2_visitor.model_table_df
        df.to_csv(out_file, index=False)

    def to_dict(self):
        """_summary_"""
        dd = {}
        for pre, fill, node in RenderTree(self):
            if isinstance(node, Element) or isinstance(node, Relationship):
                index = node.idx
                vv = node.to_dict()
                dd[index] = vv
        return dd

    def to_dot(self, out_dir=None, file=None):
        """_summary_

        Args:
            out_dir (_type_): _description_
        """
        # Create the output directory if it doesn't exist, set file name
        out_file = self._out_file_handler(".dot", out_dir, file)
        # Write the dot file
        DotExporter(self).to_dotfile(out_file)

    def to_JSON(self, out_dir=None, file=None):
        """_summary_

        Args:
            out_dir (_type_): _description_
        """

        def for_non_serializable_obj(obj):
            """Some objects in the model are not serializable. This function is
            passed to the JsonExporter to handle these objects. It returns the
            type of the object, which is recorded in the JSON. Note that the
            contents of the object are lost. This occurs for the Antlr4 visitor
            because it has a Stream object that is not serializable.

            Note that I have passed the repr of the object to the JSON. This is
            dangerous for complex objects, but works well for simple objects
            like Python type.

            TODO: Note this is a bit of a hack! It would be great to serailize
            the visitor. Perhaps we can somehow ignore the Stream object? Not a
            problem that needs to be solved right now, but should be addressed
            before production use.
            """
            return repr(type(obj))

        # Create the output directory if it doesn't exist, set file name
        out_file = self._out_file_handler(".json", out_dir, file)

        # Write the JSON file
        exporter = JsonExporter(
            indent=2, sort_keys=True, default=for_non_serializable_obj
        )
        data = exporter.export(self)
        with open(out_file, "w", encoding="utf-8") as outfile:
            outfile.write(data)

    def to_png(self, out_dir=None, file=None):
        """_summary_
        Invokes the graphviz library to render the model to a PNG file.
        TODO: Rewrite this so that we can use the unflatten GraphViz tool to
        make better looking graphs. See StackOverflow question:
        stackoverflow.com/questions/73262051/how-can-i-adjust-a-graphviz-render

        Perhaps build a superclass of DotExporter?
        Args:
            out_dir (_type_): _description_
        """
        # Create the output directory if it doesn't exist, set file name
        out_file = self._out_file_handler(".png", out_dir, file)
        # Write the image of the graph
        DotExporter(self).to_picture(out_file)

    def to_txt(self, out_dir=None, file=None):
        """_summary_

        Args:
            out_dir (_type_): _description_
        """
        # Create the output directory if it doesn't exist, set file name
        out_file = self._out_file_handler(".txt", out_dir, file)
        # Write the text file
        with open(out_file, "w", encoding="utf-8") as outfile:
            outfile.write(str(self))

    def _out_file_handler(self, ext, out_dir=None, file=None):
        """_summary_

        Args:
            out_dir (_type_): _description_
        """
        # Create the output directory if it doesn't exist, set file name
        out_dir = "." if out_dir is None else out_dir
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        file = self.input_file if file is None else file
        root = os.path.splitext(os.path.basename(file))[0]
        out_file = os.path.join(out_dir, root + ext)
        return out_file

    def __str__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        ss = ""
        for pre, fill, node in RenderTree(self.root):

            if isinstance(node, Model):

                idx, name = NODE_ROOT_NAME, ""
            else:
                idx, name = node.idx, node.name

            ss += "{}[{}]: {}\n".format(pre, idx, name)
        return ss
