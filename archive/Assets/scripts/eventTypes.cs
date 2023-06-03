using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class eventTypes:MonoBehaviour {

    [Serializable]
    public struct dialougeEvent {
        public string character;      //Name of character who's talking
        public string animation;      //Name of animation to play, automatically includes talking animation
        public string nextType1;      //What the next event's type will be
        public string nextType2;      //What the next event's type will be
        public string nextType3;      //What the next event's type will be
        public string nextType4;      //What the next event's type will be
        public string nextType;       //What the next event's type will be
        public float timeout;         //Number of seconds options will be pickable for. Set to any negative value to disable.

        public List<string> dialogue; //Lines of dialoge for the character to say.
        public string question;       //Last line of dialouge to be said. Shows when responses are displayed.
        public string option1;        //Player response option 1.
        public string option2;        //Player response option 2.
        public string option3;        //Player response option 3.
        public string option4;        //Player response option 4.

        public string target1;        //Next event to play if player picks option 1.
        public string target2;        //Next event to play if player picks option 2.
        public string target3;        //Next event to play if player picks option 3.
        public string target4;        //Next event to play if player picks option 4.
        public string targetDefault;  //Next event to play if the options time out.
    }

    [Serializable]
    public struct setVarEvent {
        public int strID;
        public int intID;
        public int floatID;
        public int boolID;
        public int inventorySlot;

        public string strValue;
        public int intValue;
        public float floatValue;
        public bool boolValue;
        public string itemName;

        public string nextType;
        public string targetDefault;
    }

    [Serializable]
    public struct varVarStr {
        public int var1id;
        public int var2id;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varVarInt {
        public int var1id;
        public int var2id;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varVarFloat {
        public int var1id;
        public int var2id;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varVarBool {
        public int var1id;
        public int var2id;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varVarInv {
        public int var1id;
        public int var2id;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varValueStr {
        public int var;
        public string value;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varValueInt {
        public int var;
        public int value;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varValueFloat {
        public int var;
        public float value;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varValueBool {
        public int var;
        public bool value;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct varValueInv {
        public int var;
        public string value;

        public string nextType1;
        public string nextType2;
        public string target1;
        public string target2;
    }

    [Serializable]
    public struct dayCutscene {
        public string title;
        public string subtitle;
        public int dayNumber;
        public string weather;

        public string nextType;
        public string targetDefault;
    } 

    [Serializable]
    public struct sceneTransition {
        public string scene;
        public List<string> characters;
        public List<bool> sides;

        public string nextType;
        public string targetDefault;
    }

    [Serializable]
    public struct musicTransition {
        public float fadeout;
        public float fadein;
        public string track;

        public string nextType;
        public string targetDefault;
    }


    public void Start() {
        dialougeEvent testing = new dialougeEvent();
        testing.character = "a";
        testing.animation = "b";
        testing.nextType1 = "c";
        testing.nextType2 = "d";
        testing.nextType3 = "e";
        testing.nextType4 = "f";
        testing.nextType = "g";
        testing.timeout = 0;

        testing.dialogue = new List<string>();
        testing.dialogue.Add("h");
        testing.question = "i";
        testing.option1 = "j";
        testing.option2 = "k";
        testing.option3 = "l";
        testing.option4 = "m";

        testing.target1 = "n";
        testing.target2 = "o";
        testing.target3 = "p";
        testing.target4 = "q";
        testing.targetDefault = "r";

        string outputTest = JsonUtility.ToJson(testing);
        print(outputTest);
        testing = JsonUtility.FromJson<dialougeEvent>("{\"character\": \"\", \"animation\": \"\", \"timeout\": 0.0, \"dialogue\": [], \"question\": \"\", \"option1\": \"\", \"option2\": \"\", \"option3\": \"\", \"option4\": \"\", \"target1\": \"END\", \"nextType1\": \"END\", \"target2\": \"END\", \"nextType2\": \"END\", \"target3\": \"END\", \"nextType3\": \"END\", \"target4\": \"END\", \"nextType4\": \"END\", \"targetDefault\": \"END\", \"nextType\": \"END\"}");
        outputTest = JsonUtility.ToJson(testing);
        print(outputTest);
    }
}
