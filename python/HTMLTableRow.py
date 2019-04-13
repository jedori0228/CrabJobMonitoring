import os

class HTMLTableRow:

  def __init__(self, varName, color='black', align='center'):

    self.VarName = varName
    self.Color = color
    self.Align = align

  def GetHTMLLine(self, content):

    out = '    <td align="'+self.Align+'"><font color='+self.Color+'>'+content+'</font></td>'+'\n'
    return out


