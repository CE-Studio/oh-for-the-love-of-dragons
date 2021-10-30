using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class genericTextboxControler:MonoBehaviour {

    [Serializable]
    public struct turnContent {
        public string character;
        public string animation;
        public float timeout;

        public List<string> dialogue;
        public string question;
        public string option1;
        public string option2;
        public string option3;
        public string option4;

        public string target1;
        public string target2;
        public string target3;
        public string target4;
        public string targetDefault;
    }

    // Start is called before the first frame update
    void Start() {

    }

    // Update is called once per frame
    void Update() {

    }
}
