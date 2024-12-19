extends BaseGraphNode

func verify():
	print("ha")
	print(connectedTo.keys())
	for i in connectedTo.keys():
		print(i)
	if $chartype/LineEdit.text == "":
		return ["error", "Character name/ID required!"]
	if $animtype/LineEdit.text == "":
		return ["error", "Animation name/ID required!"]
	return ["ok"]
