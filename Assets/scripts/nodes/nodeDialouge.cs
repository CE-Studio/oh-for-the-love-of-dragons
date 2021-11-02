using UnityEngine;
using System.Collections.Generic;
using NodeEditorFramework;
using NodeEditorFramework.Utilities;

namespace NodeEditorFramework.Standard {
    [Node(false, "Dialouge or Choice")]
    public class nodeDialouge:Node {
        public const string ID = "nodeDialouge";
        public override string GetID { get { return ID; } }

        public override string Title { get { return "Dialouge or Choice"; } }
        public override Vector2 DefaultSize { get { return new Vector2(150, 60); } }
        public override bool AutoLayout { get { return true; } }

        [ConnectionKnob("", Direction.In)]
        public ConnectionKnob inputKnob;
        [ConnectionKnob("Output", Direction.Out)]
        public ConnectionKnob outputKnob;

        public override void NodeGUI() {

            //GUILayout.BeginHorizontal();
            //GUILayout.BeginVertical();

            inputKnob.DisplayLayout();

            //GUILayout.EndVertical();
            //GUILayout.BeginVertical();

            outputKnob.DisplayLayout();

            //GUILayout.EndVertical();
            //GUILayout.EndHorizontal();

        }

        public override bool Calculate() {
            return true;
        }
    }
}