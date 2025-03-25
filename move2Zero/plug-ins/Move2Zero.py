import sys
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class XMove2ZeroCmd(om.MPxCommand):
    kPluginCmdName = "xMove2Zero"
    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return XMove2ZeroCmd()

    def doIt(self, args):
        move_to_x_zero()

class YMove2ZeroCmd(om.MPxCommand):
    kPluginCmdName = "yMove2Zero"
    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return YMove2ZeroCmd()

    def doIt(self, args):
        move_to_y_zero()

class ZMove2ZeroCmd(om.MPxCommand):
    kPluginCmdName = "zMove2Zero"
    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return ZMove2ZeroCmd()

    def doIt(self, args):
        move_to_z_zero()

def initializePlugin(plugin):
    vendor = "Kakoi Keisuke"
    version = "1.0.0"
    pluginFn = om.MFnPlugin(plugin, vendor, version)

    try:
        pluginFn.registerCommand(
            XMove2ZeroCmd.kPluginCmdName, XMove2ZeroCmd.cmdCreator
        )
    except:
        sys.stderr.write('コマンドの登録に失敗しました。')
    try:
        pluginFn.registerCommand(
            YMove2ZeroCmd.kPluginCmdName, YMove2ZeroCmd.cmdCreator
        )
    except:
        sys.stderr.write('コマンドの登録に失敗しました。')
    try:
        pluginFn.registerCommand(
            ZMove2ZeroCmd.kPluginCmdName, ZMove2ZeroCmd.cmdCreator
        )
    except:
        sys.stderr.write('コマンドの登録に失敗しました。')
    try:
        create_ui()
    except:
        sys.stderr.write('メニューの作成に失敗しました。')

def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(
            XMove2ZeroCmd.kPluginCmdName
        )
    except:
        sys.stderr.write('コマンドの除去に失敗しました')
    try:
        pluginFn.deregisterCommand(
            YMove2ZeroCmd.kPluginCmdName
        )
    except:
        sys.stderr.write('コマンドの除去に失敗しました')
    try:
        pluginFn.deregisterCommand(
            ZMove2ZeroCmd.kPluginCmdName
        )
    except:
        sys.stderr.write('コマンドの除去に失敗しました')
    try:
        delete_ui()
    except:
        sys.stderr.write('メニューの削除に失敗しました。')

def create_ui():
    main_window = mel.eval('$gmw = $gMainWindow')
    if cmds.menu('Move2Zero', exists=True):
        cmds.deleteUI('Move2Zero')
    custom_menu = cmds.menu('Move2Zero', parent=main_window, label='Move2Zero', tearOff=True)
    cmds.menuItem(
        label='X=0 に移動',
        parent=custom_menu,
        command='cmds.xMove2Zero()',
        image='menuItemIcon_x.svg',
        annotation='オブジェクトの端が X=0 となるように移動させます。'
    )
    cmds.menuItem(
        label='Y=0 に移動',
        parent=custom_menu,
        command='cmds.yMove2Zero()',
        image='menuItemIcon_y.svg',
        annotation='オブジェクトの端が Y=0 となるように移動させます。'
    )
    cmds.menuItem(
        label='Z=0 に移動',
        parent=custom_menu,
        command='cmds.zMove2Zero()',
        image='menuItemIcon_z.svg',
        annotation='オブジェクトの端が Z=0 となるように移動させます。'
    )

def delete_ui():
    if cmds.menu('Move2Zero', exists=True):
        cmds.deleteUI('Move2Zero')

def move_to_x_zero():
    obj = get_target_object()
    amount = get_transform_amount(obj, 0)
    for i in range(len(obj)):
        move_amount = amount[i] * -1
        cmds.move(move_amount, 0, 0, relative=True)

def move_to_y_zero():
    obj = get_target_object()
    amount = get_transform_amount(obj, 1)
    for i in range(len(obj)):
        move_amount = amount[i] * -1
        cmds.move(0, move_amount, 0, relative=True)

def move_to_z_zero():
    obj = get_target_object()
    amount = get_transform_amount(obj, 2)
    for i in range(len(obj)):
        move_amount = amount[i] * -1
        cmds.move(0, 0, move_amount, relative=True)

def get_target_object():
    target_object = cmds.ls(selection=True, transforms=True)
    if len(target_object) == 0:
        cmds.warning('移動させるオブジェクトを指定してください。')
    return target_object

def get_transform_amount(object_list, move_axis):
    transform_amount = []
    for i in range(len(object_list)):
        vtx = cmds.ls(object_list[i] + '.vtx[*]', flatten=True)
        min_vtx = cmds.pointPosition(vtx[0], world=True)[move_axis]
        for j in range(len(vtx)):
            now_vtx = cmds.pointPosition(vtx[j], world=True)[move_axis]
            if min_vtx > now_vtx:
                min_vtx = now_vtx
        transform_amount.append(min_vtx)
    return transform_amount