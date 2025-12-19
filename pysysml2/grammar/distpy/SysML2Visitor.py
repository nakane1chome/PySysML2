# Generated from SysML2.g4 by ANTLR 4.10
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SysML2Parser import SysML2Parser
else:
    from SysML2Parser import SysML2Parser

# This class defines a complete generic visitor for a parse tree produced by SysML2Parser.

class SysML2Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by SysML2Parser#model.
    def visitModel(self, ctx:SysML2Parser.ModelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#element.
    def visitElement(self, ctx:SysML2Parser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#namespace.
    def visitNamespace(self, ctx:SysML2Parser.NamespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#sysml2_package.
    def visitSysml2_package(self, ctx:SysML2Parser.Sysml2_packageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#part_blk.
    def visitPart_blk(self, ctx:SysML2Parser.Part_blkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#part.
    def visitPart(self, ctx:SysML2Parser.PartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#part_def.
    def visitPart_def(self, ctx:SysML2Parser.Part_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#part_def_specializes.
    def visitPart_def_specializes(self, ctx:SysML2Parser.Part_def_specializesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#port.
    def visitPort(self, ctx:SysML2Parser.PortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#port_def.
    def visitPort_def(self, ctx:SysML2Parser.Port_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#port_blk.
    def visitPort_blk(self, ctx:SysML2Parser.Port_blkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#use_case_blk.
    def visitUse_case_blk(self, ctx:SysML2Parser.Use_case_blkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#use_case_def.
    def visitUse_case_def(self, ctx:SysML2Parser.Use_case_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#part_objective_blk.
    def visitPart_objective_blk(self, ctx:SysML2Parser.Part_objective_blkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#objective_def.
    def visitObjective_def(self, ctx:SysML2Parser.Objective_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#subject_def.
    def visitSubject_def(self, ctx:SysML2Parser.Subject_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#include.
    def visitInclude(self, ctx:SysML2Parser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#include_blk.
    def visitInclude_blk(self, ctx:SysML2Parser.Include_blkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#message.
    def visitMessage(self, ctx:SysML2Parser.MessageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#message_expr.
    def visitMessage_expr(self, ctx:SysML2Parser.Message_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature.
    def visitFeature(self, ctx:SysML2Parser.FeatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#connection.
    def visitConnection(self, ctx:SysML2Parser.ConnectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#connection_blk.
    def visitConnection_blk(self, ctx:SysML2Parser.Connection_blkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#end_part.
    def visitEnd_part(self, ctx:SysML2Parser.End_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#enum_def.
    def visitEnum_def(self, ctx:SysML2Parser.Enum_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#enum_value.
    def visitEnum_value(self, ctx:SysML2Parser.Enum_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#connect.
    def visitConnect(self, ctx:SysML2Parser.ConnectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#connect_expr.
    def visitConnect_expr(self, ctx:SysML2Parser.Connect_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature_attribute_def.
    def visitFeature_attribute_def(self, ctx:SysML2Parser.Feature_attribute_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature_attribute_redefines.
    def visitFeature_attribute_redefines(self, ctx:SysML2Parser.Feature_attribute_redefinesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature_part_specializes.
    def visitFeature_part_specializes(self, ctx:SysML2Parser.Feature_part_specializesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature_part_specializes_subsets.
    def visitFeature_part_specializes_subsets(self, ctx:SysML2Parser.Feature_part_specializes_subsetsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature_item_def.
    def visitFeature_item_def(self, ctx:SysML2Parser.Feature_item_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature_item_ref.
    def visitFeature_item_ref(self, ctx:SysML2Parser.Feature_item_refContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#feature_actor_specializes.
    def visitFeature_actor_specializes(self, ctx:SysML2Parser.Feature_actor_specializesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#comment.
    def visitComment(self, ctx:SysML2Parser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#comment_unnamed.
    def visitComment_unnamed(self, ctx:SysML2Parser.Comment_unnamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#comment_named.
    def visitComment_named(self, ctx:SysML2Parser.Comment_namedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#comment_named_about.
    def visitComment_named_about(self, ctx:SysML2Parser.Comment_named_aboutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#doc.
    def visitDoc(self, ctx:SysML2Parser.DocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#doc_unnamed.
    def visitDoc_unnamed(self, ctx:SysML2Parser.Doc_unnamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#doc_named.
    def visitDoc_named(self, ctx:SysML2Parser.Doc_namedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#statement.
    def visitStatement(self, ctx:SysML2Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SysML2Parser#import_package.
    def visitImport_package(self, ctx:SysML2Parser.Import_packageContext):
        return self.visitChildren(ctx)



del SysML2Parser