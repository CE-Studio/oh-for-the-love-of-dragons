using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class genericTextboxControler:MonoBehaviour {

    [Serializable]
    public struct turnContent {
        public string character;      //Name of character who's talking
        public string animation;      //Name of animation to play, automatically includes talking animation
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

    // Start is called before the first frame update
    void Start() {

    }

    // Update is called once per frame
    void Update() {

    }
}
