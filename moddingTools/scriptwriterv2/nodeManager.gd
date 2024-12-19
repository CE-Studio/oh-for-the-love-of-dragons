extends Node


var nodes:Array[PackedScene] = []
var nodeNames:PackedStringArray = []


# Called when the node enters the scene tree for the first time.
func _ready():
	var dir := DirAccess.get_files_at("res://nodes")
	for i in dir:
		nodes.append(load("res://nodes/" + i))
	for i in nodes:
		var h:GraphNode = i.instantiate()
		nodeNames.append(h.title)
		h.free()
	print(nodeNames[0])


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
