using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Firebase;
using Firebase.Extensions;
using Firebase.Database;
using System.Globalization;
using LSL;

public class Listener : MonoBehaviour
{
    DatabaseReference reference;
    StreamInfo inf;
    StreamOutlet outl;

    // Start is called before the first frame update
    void Start()
    {
        inf = new StreamInfo("Test2", "Markers", 1, 0, channel_format_t.cf_string, "giu4569");
        outl = new StreamOutlet(inf);

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

        // Set up listener for new messages
        SubscribeToUpdates();
    }

private void SubscribeToUpdates()
    {
        // Assuming data is stored under a node named "messages"
        DatabaseReference messagesRef = reference.Child("messages");

        messagesRef.ChildAdded += (object sender, ChildChangedEventArgs args) =>
        {
            if (args.DatabaseError != null)
            {
                Debug.LogError(args.DatabaseError.Message);
                return;
            }

            // Print the received data
            string string_to_send = "Event 1 - Start";
            SendEventMarkerLSL(string_to_send);

            Debug.Log("Received update: " + args.Snapshot.GetRawJsonValue());

            // Remove the message from Firebase after processing
            args.Snapshot.Reference.RemoveValueAsync().ContinueWithOnMainThread(task => {
                if (task.IsFaulted)
                {
                    Debug.LogError("Error removing message: " + task.Exception.ToString());
                }
            });
        };
    }

    public void SendEventMarkerLSL(string eventName)  {
        string[] eventArray = new string[] { eventName };
        outl.push_sample(eventArray);
        Debug.Log("event logged: "+ eventName);
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
    
    void Update()
    {
        // Optional: Handle user input or other per-frame logic
    }
}