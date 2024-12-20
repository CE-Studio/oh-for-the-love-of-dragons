extends BaseGraphNode

func verify():
	if $chartype/LineEdit.text == "":
		return ["error", "Character name/ID required!"]
	if $animtype/LineEdit.text == "":
		return ["error", "Animation name/ID required!"]
	return ["ok"]
