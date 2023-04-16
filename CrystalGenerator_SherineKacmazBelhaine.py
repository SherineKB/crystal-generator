""" BLENDER VERSION : 3.3.4"""

""" Crystal Generator """

import bpy
import random

# Delete meshes
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
    

""" Program for the "pure" crystals creation """

class CrystalGenerator():            
    
    def __init__(self, crystal_amount):
        
        # The slider contains the variable crystal_amount
        self.cA = crystal_amount    
    
    def crystal(self):              
                
        # Random numbers
        randomNumber = random.randint(1, 180)        
        randomScale = random.randint(0, 1)
        
        # Crystal base
        bpy.ops.mesh.primitive_uv_sphere_add(segments=4, ring_count=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1.7))
        bpy.context.active_object.name = "crystal"                
        
        # Modifier - Bevels on vertices 
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].affect = 'VERTICES'
        bpy.context.object.modifiers["Bevel"].width = 0.05
        
        # Switch to Edit Mode
        bpy.ops.object.editmode_toggle()
        
        # Deselect the mesh
        bpy.ops.mesh.select_all(action='DESELECT')

        # Select random verticies
        bpy.ops.mesh.select_random(seed = randomNumber)
        
        # Modify randomly the position of the vertices
        bpy.ops.transform.vertex_random(offset=0.3, uniform=0, normal=1)        
                
        # Switch to Object Mode
        bpy.ops.object.editmode_toggle()       
        
        # Begin the slider at 1, it doesn't consider the 0. Call the crystal amount variable.        
        for i in range (1, self.cA):
            bpy.ops.object.duplicate_move_linked()
        
        # Select the mesh  
        bpy.ops.object.select_all(action='SELECT')
        
        # Transform randomly the crystal 
        bpy.ops.object.randomize_transform(random_seed=randomNumber, rot=(1, 1, 1), scale_even=True, scale=(randomScale, 1, 1))
  

        """ MATERIAL CREATION """
        
        # Create a new shader named CrystalMat
        material_crystal = bpy.data.materials.new(name="CrystalMat")
        material_crystal.use_nodes = True 
        
        #Attribute the material to selected object
        bpy.context.object.active_material = material_crystal
                
        # NODES IN PYTHON
        
        # material outpout
        material_output = material_crystal.node_tree.nodes.get('Material Output')
        material_output.location = (2800, 0)
        
        # principled BSDF
        principled_BSDF = material_crystal.node_tree.nodes.get('Principled BSDF')
        principled_BSDF.location = (2500, 0)
        principled_BSDF.subsurface_method = 'RANDOM_WALK'       
        principled_BSDF.inputs[17].default_value = (0.910)
        
        # bump node 1
        bump1 = material_crystal.node_tree.nodes.new('ShaderNodeBump')
        bump1.location = (2200, -600)
        bump1.inputs[0].default_value = (0.060)
        
        # bump node 2
        bump2 = material_crystal.node_tree.nodes.new('ShaderNodeBump')
        bump2.location = (1900, -100)
        bump2.inputs[0].default_value = (0.1)
        
        
        # color ramp 1        
        color_ramp1 = material_crystal.node_tree.nodes.new('ShaderNodeValToRGB')
        color_ramp1.location = (1800, -350)
        
        color_ramp1.color_ramp.elements[0].position = (0.382)
        color_ramp1.color_ramp.elements[0].color = (0, 0, 0, 1)
                        
        color_ramp1.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        # color ramp 2        
        color_ramp2 = material_crystal.node_tree.nodes.new('ShaderNodeValToRGB')
        color_ramp2.location = (1800, -600)
        
        color_ramp2.color_ramp.elements[0].position = (0.359)
        color_ramp2.color_ramp.elements[0].color = (0, 0, 0, 1)
        
        color_ramp2.color_ramp.elements[1].position = (0.486)
        color_ramp2.color_ramp.elements[1].color = (1, 1, 1, 1)
        
        # multiply
        multiply = material_crystal.node_tree.nodes.new('ShaderNodeMath')
        multiply.location = (1600, -650)
        multiply.operation = 'MULTIPLY'
        
        
        # noise texture 1
        noise_texture1 = material_crystal.node_tree.nodes.new('ShaderNodeTexNoise')
        noise_texture1.location = (1400, -300)
        
        noise_texture1.inputs[2].default_value = (1.7)
        noise_texture1.inputs[3].default_value = (15.0)
        noise_texture1.inputs[4].default_value = (0.067)
        noise_texture1.inputs[5].default_value = (0)
        
        # noise texture 2
        noise_texture2 = material_crystal.node_tree.nodes.new('ShaderNodeTexNoise')
        noise_texture2.location = (1400, -600)
        
        noise_texture2.inputs[2].default_value = (7)
        noise_texture2.inputs[3].default_value = (15.0)
        noise_texture2.inputs[4].default_value = (0.5)
        noise_texture2.inputs[5].default_value = (0)
          
        # texture coordinate
        texture_coordinate = material_crystal.node_tree.nodes.new('ShaderNodeTexCoord')
        texture_coordinate.location = (1100,-300)                 
        
        # RGB 
        rgb = material_crystal.node_tree.nodes.new('ShaderNodeRGB')
        rgb.location = (2200, 0)
        
        
        #CONNEXIONS
        
        # Texture Coordinate
        material_crystal.node_tree.links.new(texture_coordinate.outputs[3], noise_texture1.inputs[0])
        material_crystal.node_tree.links.new(texture_coordinate.outputs[3], noise_texture2.inputs[0])
        
        # Noise Texture 1
        material_crystal.node_tree.links.new(noise_texture1.outputs[1], bump2.inputs[2])
        
        # Noise Texture 2
        material_crystal.node_tree.links.new(noise_texture2.outputs[0], color_ramp1.inputs[0])
        material_crystal.node_tree.links.new(noise_texture2.outputs[0], multiply.inputs[0])
        
        # Multiply 
        material_crystal.node_tree.links.new(multiply.outputs[0], color_ramp2.inputs[0])
        
        # Bump 2 
        material_crystal.node_tree.links.new(bump2.outputs[0], bump1.inputs[3])
        
        # Color Ramp 1
        material_crystal.node_tree.links.new(color_ramp1.outputs[0], principled_BSDF.inputs[9])  
         
        # Color Ramp 2
        material_crystal.node_tree.links.new(color_ramp2.outputs[0], bump1.inputs[2])        
        
        #Bump 1             
        material_crystal.node_tree.links.new(bump1.outputs[0], principled_BSDF.inputs[5])
        material_crystal.node_tree.links.new(bump1.outputs[0], principled_BSDF.inputs[22])

        # Principled BSDF
        material_crystal.node_tree.links.new(principled_BSDF.outputs[0], material_output.inputs[0])
        
        # RGB
        material_crystal.node_tree.links.new(rgb.outputs[0], principled_BSDF.inputs[0])
        
        # Deselect
        bpy.ops.object.select_all(action='DESELECT')

""" UI """
# Inside the button
class CrystalOperator(bpy.types.Operator):
    
    bl_idname = 'opr.object_crystal_operator'
    bl_label = 'Crystal Operator'
        
    def execute(self,context) :
        
        # Each time the execute is loaded, it delete the old crystals
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Delete the old material
        delete = bpy.data.materials.get("CrystalMat")
        
        if delete:
            bpy.data.materials.remove(delete, do_unlink=True)
        
        # to execute the program of the crystal creation each time the button is pressed
        callClassCrystal()
        return {'FINISHED'}

# Create a fonction related to the slider initialisation. When "crysA" is called, it will be initialised in the slider.
def callClassCrystal():    
    
    # Variable contains the slider
    crysA = bpy.context.window_manager.crystal_amount
    
    # The class which contains the main program is initialized into the slider.          
    CrystalGen = CrystalGenerator(crysA)
    # Execute the "crystal" definition from the class
    CrystalGen.crystal()
    
# Create the slider    
bpy.types.WindowManager.crystal_amount = bpy.props.IntProperty(name="Crystal Amount",min = 1, max = 5, default = 4)    
    
# PANELS
class CrystalPanel(bpy.types.Panel):
    
    # Tab title
    bl_category = "Generator"    
    bl_description = ("Crystal Generator")
    
    # Panel title
    bl_label = 'Crystal Generator'
    bl_idname = 'VIEW3D_PT_CrystalOperator'   
    
    # UI in the 3D view
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    # Icon panel
    def draw_header(self, context):
        self.layout.label(icon="PMARKER")
        
    # Set a panel    
    def draw(self, context):
        
        # Create a panel
        l = self.layout
        
        # Create a column in the panel
        c = l.column()
        
        # Slider
        c.prop(context.window_manager, "crystal_amount")
        
        # Generate Button
        c.operator('opr.object_crystal_operator', text='Generate')
        
        

# Register my panel in Blender
def register():
    bpy.utils.register_class(CrystalPanel)
    bpy.utils.register_class(CrystalOperator)
    
# Unset the panel when Blender is closed
def unregister():
    bpy.utils.unregister_class( CrystalPanel)
    bpy.utils.unregister_class(CrystalOperator)

# Load the panel creation
if __name__ == '__main__':
    register()
