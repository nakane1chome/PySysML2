from typing import get_type_hints
import uuid

import pandas as pd

from pysysml2.grammar.distpy.SysML2Lexer import SysML2Lexer
from pysysml2.grammar.distpy.SysML2Parser import SysML2Parser
from pysysml2.grammar.distpy.SysML2Visitor import SysML2Visitor
from pysysml2.grammar import antlr4_helper

# Module Variables
_SML2_KWS = antlr4_helper.build_lexer_literal_enum(SysML2Lexer, "SysML2KewordsEnum")
_DLMTR_UNDRSCR = "_"
_DLMTR_AT = "@"
_DLMTR_FQN = _SML2_KWS.KW_SYM_FQN.value
# Variable names for additions to the Antlr4 context objects
_IDX_CTX_NAME = "_PySysML2_IDX"
_IDX_PARENT_CTX_NAME = "_PySysML2_IDX_PARENT"
_UUID_CTX_NAME = "_PySysML2_UUID"
_UUID_PARENT_CTX_NAME = "_PySysML2_UUID_PARENT"
_ELMNT_ID_CTX_NAME = "_PySysML2_NAME"
_SYSML2_TYPE_NAME = "_PySysML2_SYSML2_TYPE"
_FQN_TAG_NAME = "_PySysML2_FQN_TAGGED"
_FQN_NAME = "_PySysML2_FQN"
# PySysML2 specific tags and names
_UNNAMED_ELEMENT_NAME = "PySysML2_GENERATED_NAME"
_SYSML2_RELATIONSHIP_SPECIALIZES = "specializes"
_SYSML2_RELATIONSHIP_REDEFINES = "redefines"
_SYSML2_RELATIONSHIP_ABOUT = "about"
_SYSML2_RELATIONSHIP_REFERENCES = "references"


class ModelTreeSysML2Visitor(SysML2Visitor):
    def __init__(self) -> None:
        """_summary_"""
        super().__init__()
        self.model_table_dict = {}
        self.element_count = 0
        self.element_ctxs = {}
        self.idxs = []
        self.parser_contexts_dict = antlr4_helper.build_parser_context_names_enum(
            SysML2Parser, "Contexts"
        )
        self.focused_contexts = self._map_systems_types()
        self.names_to_idxs_dict = {}

    @property
    def model_table_df(self):
        return pd.DataFrame.from_dict(self.model_table_dict, orient="index")

    def _model_table_builder(self, ctx):
        """ " Builds a model table dictionary. This dictionary is the primary
        interface to the PySysML2 Model class and all other serialization
        methods. This function is called by all visit methods overriden in
        ModelTreeSysML2Visitor everytime a relevant context is visited.

        Args:
            ctx (_type_): _description_

        Raises:
            Exception: _description_
            Exception: _description_
            Exception: _description_
        """
        # Handle element indices and global UUIDs
        ########################################################################
        if self.element_count in self.idxs:
            raise Exception(
                "Duplicate element index {} \
                came as a complete surprise!".format(
                    self.element_count
                )
            )
        self.idxs.append(self.element_count)
        if hasattr(ctx, _IDX_CTX_NAME):
            raise Exception(
                "Visited element index {} \
                twice, which came as a complete surprise!".format(
                    self.element_count
                )
            )
        # Save the UID in the ctx object for easy access, using the setattr and
        # getattr functions to support the use of the UID_TAG_NAME
        setattr(ctx, _IDX_CTX_NAME, self.element_count)
        idx = getattr(ctx, _IDX_CTX_NAME)
        # Retrieve the parent UID and record it in the ctx object
        idx_parent = self._get_parent_IDX(ctx)
        if hasattr(ctx, _IDX_PARENT_CTX_NAME):
            raise Exception(
                "Visited element index {} \
                twice, which came as a complete surprise!".format(
                    self.element_count
                )
            )
        setattr(ctx, _IDX_PARENT_CTX_NAME, idx_parent)
        # Global Universally Unique Identifier (UUID)
        # Generate and save the UUID in the ctx object
        uuid_ctx = str(uuid.uuid4())
        if hasattr(ctx, _UUID_CTX_NAME):
            raise Exception(
                "Visited element index {} \
                twice, which came as a complete surprise!".format(
                    self.element_count
                )
            )
        setattr(ctx, _UUID_CTX_NAME, uuid_ctx)
        # Retrieve the parent UUID and record it in the ctx object
        uuid_parent_ctx = self._get_parent_UUID(ctx)
        if hasattr(ctx, _UUID_PARENT_CTX_NAME):
            raise Exception(
                "Visited element index {} \
                twice, which came as a complete surprise!".format(
                    self.element_count
                )
            )
        setattr(ctx, _UUID_PARENT_CTX_NAME, uuid_parent_ctx)

        # Context type, e.g. 'Sysml2_packageContext'
        # Context types trace back to the SysML2 grammar rules
        context_type = type(ctx).__name__
        names = self._get_ID(ctx)
        name = self._tag_name(names[0], idx, idx_parent)
        self.names_to_idxs_dict[name] = idx  # TODO: replace when better UIDs
        # Save the PySysML2 generated name in the ctx object for easy access
        # An element should not already have a PySysML2 generated name
        if hasattr(ctx, _ELMNT_ID_CTX_NAME):
            raise Exception(
                "Named element UID {} \
                twice, which came as a complete surprise!".format(
                    self.element_count
                )
            )
        setattr(ctx, _ELMNT_ID_CTX_NAME, name)
        # Record the ctx object for this element in the element_ctxs dictionary
        self.element_ctxs[getattr(ctx, _IDX_CTX_NAME)] = names[0], ctx
        # Get the name of the parent element generated by PySysML2.
        # If the parent element is None, then the parent element is the root,
        # and the parent element name is _ROOT_ELEMENT_NAME

        name_parent = (
            getattr(self.element_ctxs[idx_parent][1], _ELMNT_ID_CTX_NAME)
            if idx_parent is not None
            else None
        )

        # Save Fully Qualified Name
        fqn, fqn_tagged, tree_level = self._get_fully_qualified_name(ctx)
        if hasattr(ctx, _FQN_TAG_NAME):
            raise Exception(
                "Fully qualified name UID {} \
                twice, which came as a complete surprise!".format(
                    self.element_count
                )
            )
        if hasattr(ctx, _FQN_NAME):
            raise Exception(
                "Fully qualified name UID {} \
                twice, which came as a complete surprise!".format(
                    self.element_count
                )
            )
        setattr(ctx, _FQN_NAME, fqn)
        setattr(ctx, _FQN_TAG_NAME, fqn_tagged)
        # Increment the element count
        self.element_count += 1

        # Handle types, constants, multiplicity, text, etc
        value_types = self._get_TYPE(ctx)
        constants = self._get_CONSTANT(ctx)
        multiplicity = self._get_MULTIPLICITY(ctx)
        comment_texts = self._get_comment_text(ctx)
        comment_text = (
            comment_texts[0].strip("/*\\") if comment_texts[0] is not None else None
        )
        # Record the keywords for this block of Sysml2 code
        keywords = self._get_keywords(context_type)
        # Handle related elements
        ########################################################################
        # KLUDGE: This is a hack to get a quick solution to the problem of
        # recognizing relationship elements. The thinking here is that a
        # code block specifying a relationship will have multiple identifiers.
        # This is also the reason that context componets are cast as a list.
        # TODO: Find a better solution to handling and recording relationships!
        # TODO: (20240805) HANDLE ALL LOGIC FOR RELATIONSHIP IN VISITOR FUNCTION
        # Leaving existing in for now, but connect relationship is handled correctly
        
        related_element_name_root = names[1] if len(names) > 1 else None
        related_element_name, idx_related_element = (
            self._get_related_element_name_idx(related_element_name_root)
            if related_element_name_root is not None
            else (None, None)
        )
        # Handle redefines kw - a type of relationship
        if _SML2_KWS.KW_REDEFINES.value in keywords:
            (
                related_element_name,
                idx_related_element,
            ) = self._get_related_element_name_idx(name)
        
        # Handle connect relationship
        if hasattr(ctx, "PySysML2_source_ids") or hasattr(ctx, "PySysML2_target_ids"):
            related_element_name = []
            related_element_name.append(getattr(ctx, "PySysML2_source_ids"))
            related_element_name.append(getattr(ctx, "PySysML2_target_ids"))
        # Handle message relationship
        if hasattr(ctx, "PySysML2_of_ids") or hasattr(ctx, "PySysML2_from_ids") or hasattr(ctx, "PySysML2_to_ids"):
            related_element_name = []
            related_element_name.append(getattr(ctx, "PySysML2_of_ids"))
            related_element_name.append(getattr(ctx, "PySysML2_from_ids"))
            related_element_name.append(getattr(ctx, "PySysML2_to_ids"))

        # Record the data for this element in the model table dictionary
        self.model_table_dict[idx] = {
            "name": name,
            "sysml2_type": getattr(ctx, _SYSML2_TYPE_NAME),
            "parent": name_parent,
            "idx": idx,
            "uuid": uuid_ctx,
            "idx_parent": idx_parent,
            "uuid_parent": uuid_parent_ctx,
            "idx_related_element": idx_related_element,
            "related_element_name": related_element_name,
            "value_types": value_types[0],
            "constants": constants,
            "multiplicity": multiplicity[0],
            "context_type": context_type,
            "keywords": keywords,
            "fully_qualified_name": fqn,
            "fully_qualified_name_tagged": fqn_tagged,
            "tree_level": tree_level,
            "element_text": comment_text,
        }

    def _map_systems_types(self):
        funs = antlr4_helper.get_overridden_methods(ModelTreeSysML2Visitor)
        contexts = [
            get_type_hints(getattr(self, fun))["ctx"].__name__
            for fun in funs
            if fun.startswith("visit")
        ]
        return contexts

    def _tag_name(self, name, uid, uid_parent):
        name = (
            "{}{}{}{}{}".format(
                _UNNAMED_ELEMENT_NAME, _DLMTR_UNDRSCR, uid, _DLMTR_UNDRSCR, uid_parent
            )
            if name is None
            else name
        )
        return "{}{}{}{}{}".format(name, _DLMTR_AT, uid, _DLMTR_UNDRSCR, uid_parent)

    def _get_fully_qualified_name(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """

        ctxs = []  # Initialize the list of contexts
        uid = getattr(ctx, _IDX_CTX_NAME)  # Initialize the UID
        while uid is not None and uid >= 0:  # While the UID is valid
            # Append the context and update from parent
            ctx = self.element_ctxs[uid][1]
            uid_parent = getattr(ctx, _IDX_PARENT_CTX_NAME)
            ctxs.append(ctx)
            uid = uid_parent
        names_tagged = [getattr(ctx, _ELMNT_ID_CTX_NAME) for ctx in ctxs]
        names = [name.split(_DLMTR_AT)[0] for name in names_tagged]
        # Names should appear like Parent1:: ... ParentN::Child
        fqn = _DLMTR_FQN.join(reversed(names))
        fqn_tagged = _DLMTR_FQN.join(reversed(names_tagged))
        # The level in the tree of the element is the length of the FQN
        tree_level = len(ctxs) - 1

        return fqn, fqn_tagged, tree_level

    def _get_ID(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            ids = ctx.ID()
            if ids is None:
                return [None]
        except:
            return [None]
        if isinstance(ids, list):
            return [x.getText().strip("'\"") for x in ids]
        else:
            return [ids.getText().strip("'\"")]

    def _get_TYPE(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """

        try:
            types = ctx.TYPE()
            if types is None:
                return [None]
        except:
            return [None]
        if isinstance(types, list):
            return [x.getText().strip("'\"") for x in types]
        else:
            return [types.getText().strip("'\"")]

    def _has_parent(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """

        try:
            ctx.parentCtx
            return True
        except:
            return False

    def _get_CONSTANT(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            constants = ctx.CONSTANT()
            if constants is None:
                return [None]
        except:
            return [None]
        if isinstance(constants, list):
            return [x.getText().strip("'\"") for x in constants]
        else:
            return [constants.getText().strip("'\"")]

    def _get_MULTIPLICITY(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            multiplicity = ctx.MULTIPLICITY()
            if multiplicity is None:
                return [None]
        except:
            return [None]
        if isinstance(multiplicity, list):
            return [x.getText() for x in multiplicity]
        else:
            return [multiplicity.getText()]

    def _get_parent_ID(self, ctx):
        while self._has_parent(ctx):
            ctx = ctx.parentCtx
            try:
                ids = self._get_ID(ctx)
                if ids not in [None, [None]]:
                    return ids
            except:
                continue

        return None

    def _get_parent_IDX(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """
        while self._has_parent(ctx):
            ctx = ctx.parentCtx
            if not hasattr(ctx, _IDX_CTX_NAME):
                continue
            return getattr(ctx, _IDX_CTX_NAME)
        return None

    def _get_parent_UUID(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """
        while self._has_parent(ctx):
            ctx = ctx.parentCtx
            if not hasattr(ctx, _UUID_CTX_NAME):
                continue
            return getattr(ctx, _UUID_CTX_NAME)
        return None

    def _get_keywords(self, type_name):
        """_summary_

        Args:
            type_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        type_name = type_name.split("Context")[0]
        tags = []
        for kw in _SML2_KWS:
            # Match keyword as a whole word with underscores as boundaries
            # This prevents "port" from matching inside "import"
            kw_lower = kw.value.lower()
            type_lower = type_name.lower()

            if (
                _DLMTR_UNDRSCR + kw_lower + _DLMTR_UNDRSCR in type_lower  # _keyword_
                or type_lower.startswith(kw_lower + _DLMTR_UNDRSCR)        # keyword_ at start
                or type_lower.endswith(_DLMTR_UNDRSCR + kw_lower)          # _keyword at end
                or kw_lower == type_lower                                   # exact match
            ):
                tags.append(kw.value)
        return tags

    def _get_comment_text(self, ctx):
        """_summary_

        Args:
            ctx (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            comment = ctx.COMMENT_LONG()
            if comment is None:
                return [None]
        except:
            return [None]
        if isinstance(comment, list):
            return [x.getText() for x in comment]
        else:
            return [comment.getText()]

    def _get_related_element_name_idx(self, name):
        """_summary_

        Args:
            name (_type_): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        name_root = name.split(_DLMTR_AT)[0]
        if name_root == _UNNAMED_ELEMENT_NAME:
            raise Exception(
                "Relation to unamed element {} \
                came as a complete surprise!".format(
                    name
                )
            )
        for k, v in self.element_ctxs.items():
            if v[0] is None:
                continue
            if v[0].split(_DLMTR_AT)[0].strip() == name_root.strip():
                return getattr(v[1], _ELMNT_ID_CTX_NAME), k
        return None, None

    # Visit a parse tree produced by SysML2Parser#sysml2_package.
    def visitSysml2_package(self, ctx: SysML2Parser.Sysml2_packageContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_PACKAGE.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#part_def.
    def visitPart_def(self, ctx: SysML2Parser.Part_defContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_PART.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#part_def_specializes.
    def visitPart_def_specializes(self, ctx: SysML2Parser.Part_def_specializesContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SYSML2_RELATIONSHIP_SPECIALIZES)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#feature_attribute_def.
    def visitFeature_attribute_def(
        self, ctx: SysML2Parser.Feature_attribute_defContext
    ):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_ATTRIBUTE.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#feature_attribute_redefines.
    def visitFeature_attribute_redefines(
        self, ctx: SysML2Parser.Feature_attribute_redefinesContext
    ):
        setattr(ctx, _SYSML2_TYPE_NAME, _SYSML2_RELATIONSHIP_REDEFINES)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#feature_part_specializes.
    def visitFeature_part_specializes(
        self, ctx: SysML2Parser.Feature_part_specializesContext
    ):
        setattr(ctx, _SYSML2_TYPE_NAME, _SYSML2_RELATIONSHIP_SPECIALIZES)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#feature_part_specializes_subsets.
    def visitFeature_part_specializes_subsets(
        self, ctx: SysML2Parser.Feature_part_specializes_subsetsContext
    ):
        setattr(ctx, _SYSML2_TYPE_NAME, _SYSML2_RELATIONSHIP_SPECIALIZES)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#comment_unnamed.
    def visitComment_unnamed(self, ctx: SysML2Parser.Comment_unnamedContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_COMMENT.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#comment_named.
    def visitComment_named(self, ctx: SysML2Parser.Comment_namedContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_COMMENT.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#comment_named_about.
    def visitComment_named_about(self, ctx: SysML2Parser.Comment_named_aboutContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SYSML2_RELATIONSHIP_ABOUT)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#doc_unnamed.
    def visitDoc_unnamed(self, ctx: SysML2Parser.Doc_unnamedContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_DOC.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#doc_named.
    def visitDoc_named(self, ctx: SysML2Parser.Doc_namedContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_DOC.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#use_case_def.
    def visitUse_case_def(self, ctx: SysML2Parser.Use_case_defContext):
        setattr(
            ctx,
            _SYSML2_TYPE_NAME,
            "{}{}".format(_SML2_KWS.KW_USE.value, _SML2_KWS.KW_CASE.value),
        )
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#objective_def.
    def visitObjective_def(self, ctx: SysML2Parser.Objective_defContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_OBJECTIVE.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#feature_item_def.
    def visitFeature_item_def(self, ctx: SysML2Parser.Feature_item_defContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_ITEM.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#feature_item_ref.
    def visitFeature_item_ref(self, ctx: SysML2Parser.Feature_item_refContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SYSML2_RELATIONSHIP_REFERENCES)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#feature_actor_specializes.
    def visitFeature_actor_specializes(
        self, ctx: SysML2Parser.Feature_actor_specializesContext
    ):
        setattr(ctx, _SYSML2_TYPE_NAME, _SYSML2_RELATIONSHIP_SPECIALIZES)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#import_package.
    def visitImport_package(self, ctx: SysML2Parser.Import_packageContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_IMPORT.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#part_def.
    def visitPort_def(self, ctx: SysML2Parser.Port_defContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_PORT.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#connection.
    def visitConnection(self, ctx: SysML2Parser.ConnectionContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_CONNECTION.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#enum_def.
    def visitEnum_def(self, ctx: SysML2Parser.Enum_defContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_ENUM.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#enum_value.
    def visitEnum_value(self, ctx: SysML2Parser.Enum_valueContext):
        setattr(ctx, _SYSML2_TYPE_NAME, "enum_value")
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#part_def.
    def visitEnd_part(self, ctx: SysML2Parser.End_partContext):
        setattr(ctx, _SYSML2_TYPE_NAME,
                "{}{}".format(_SML2_KWS.KW_END.value, _SML2_KWS.KW_PART.value))
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by SysML2Parser#connect.
    def visitConnect(self, ctx: SysML2Parser.ConnectContext):
        # Extract source and target IDs
        source_expr = ctx.connect_expr(0)
        target_expr = ctx.connect_expr(1)
        
        ctx.PySysML2_source_ids = self._get_ID_from_connect_expr(source_expr)
        if len(ctx.PySysML2_source_ids) >= 2:
            ctx.PySysML2_source_ids = f"Source: {'.'.join(ctx.PySysML2_source_ids)}"
        else:
            ctx.PySysML2_source_ids = f"Source: {ctx.PySysML2_source_ids[0]}"
        ctx.PySysML2_target_ids = self._get_ID_from_connect_expr(target_expr)
        if len(ctx.PySysML2_target_ids) >= 2:
            ctx.PySysML2_target_ids = f"Target: {'.'.join(ctx.PySysML2_target_ids)}"
        else:
            ctx.PySysML2_target_ids = f"Target: {ctx.PySysML2_target_ids[0]}"
        
        
        # Existing functionality
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_CONNECT.value)
        self._model_table_builder(ctx)
        
        return self.visitChildren(ctx)

    def _get_ID_from_connect_expr(self, expr_ctx):
        """Extracts IDs from the connect_expr context."""
        ids = []
        if expr_ctx is not None:
            primary_id = expr_ctx.ID(0)
            if primary_id is not None:
                ids.append(primary_id.getText().strip("'\""))
            secondary_id = expr_ctx.ID(1)
            if secondary_id is not None:
                ids.append(secondary_id.getText().strip("'\""))
        return ids

    # Visit a parse tree produced by SysML2Parser#part_def.
    def visitInclude(self, ctx: SysML2Parser.IncludeContext):
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_INCLUDE.value)
        self._model_table_builder(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by SysML2Parser#message.
    def visitMessage(self, ctx: SysML2Parser.MessageContext):
        # Extract 'of', 'from', and 'to' message expressions
        msg_of = ctx.message_expr(0)
        msg_from = ctx.message_expr(1)
        msg_to = ctx.message_expr(2)
        
        # Process 'of' message expression
        ctx.PySysML2_of_ids = self._get_ID_from_message_expr(msg_of)
        if len(ctx.PySysML2_of_ids) >= 2:
            ctx.PySysML2_of_ids = f"Of: {'.'.join(ctx.PySysML2_of_ids)}"
        else:
            ctx.PySysML2_of_ids = f"Of: {ctx.PySysML2_of_ids[0]}"
        
        # Process 'from' message expression
        ctx.PySysML2_from_ids = self._get_ID_from_message_expr(msg_from)
        if len(ctx.PySysML2_from_ids) >= 2:
            ctx.PySysML2_from_ids = f"From: {'.'.join(ctx.PySysML2_from_ids)}"
        else:
            ctx.PySysML2_from_ids = f"From: {ctx.PySysML2_from_ids[0]}"
        
        # Process 'to' message expression
        ctx.PySysML2_to_ids = self._get_ID_from_message_expr(msg_to)
        if len(ctx.PySysML2_to_ids) >= 2:
            ctx.PySysML2_to_ids = f"To: {'.'.join(ctx.PySysML2_to_ids)}"
        else:
            ctx.PySysML2_to_ids = f"To: {ctx.PySysML2_to_ids[0]}"
        
        # Existing functionality
        setattr(ctx, _SYSML2_TYPE_NAME, _SML2_KWS.KW_MESSAGE.value)
        self._model_table_builder(ctx)
        
        return self.visitChildren(ctx)

    def _get_ID_from_message_expr(self, expr_ctx):
        """Extracts IDs from the message_expr context."""
        ids = []
        if expr_ctx is not None:
            primary_id = expr_ctx.ID(0)
            if primary_id is not None:
                ids.append(primary_id.getText().strip("'\""))
            secondary_id = expr_ctx.ID(1)
            if secondary_id is not None:
                ids.append(secondary_id.getText().strip("'\""))
        return ids