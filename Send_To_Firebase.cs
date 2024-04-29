using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Firebase;
using Firebase.Extensions;
using Firebase.Database;
using System.Globalization;
using LSL;


public class Ping : MonoBehaviour
{
    DatabaseReference reference;
    public int x = 0;
    StreamInfo inf;
    StreamOutlet outl;

    System.Guid guid = System.Guid.NewGuid();
    // Start is called before the first frame update
    void Start()
    {
        // Configure Firebase manually using your project details
        FirebaseApp app = FirebaseApp.Create(new AppOptions
        {
            // Set your Realtime Database URL
            DatabaseUrl = new System.Uri("https://med10-106e2-default-rtdb.europe-west1.firebasedatabase.app/"),
            // Set your Web API Key
            ApiKey = "AIzaSyDdOoU54hkYbKTXhRxdMRt9vV58jks58os",
            // Set your App ID
            AppId = "med10-106e2",
            // Set your Project ID
            ProjectId = "med10-106e2"
        }, "CustomFirebaseApp");

        reference = FirebaseDatabase.GetInstance(app).RootReference;
        Debug.Log(reference);
        Debug.Log("test");
        

        // Now you can use reference to send data
    }

    public void SendData(string key, string data)
    {
        
        reference.Child("messages").Child(key).SetValueAsync(data)
            .ContinueWithOnMainThread(task => {
                if (task.IsFaulted)
                {
                    Debug.LogError("Error writing to Firebase Database");
                }
                else if (task.IsCompleted)
                {
                    Debug.Log("Data sent successfully!");
                }
            });
    }

    void Update()
    {
        x += 1;
        if (Input.GetKeyDown(KeyCode.Space)) // Example trigger
        { 
            SendData("messages", "Hello from Unity!");
        }
    }

    void OnApplicationQuit()
    {
        Debug.Log("Closing outlet stream....");
        outl.Close();
        if(outl.IsClosed == true) {
            Debug.Log("Successfully Closed!");
        }
        Debug.Log("Application ending after " + Time.time + " seconds");
    }
}