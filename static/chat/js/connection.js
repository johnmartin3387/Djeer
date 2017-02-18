'use strict';

var currentUser,
    token;

$(function() {
    $("#static").modal('hide')
	
    /*$('#loginForm').modal('show');
    $('#loginForm .progress').hide();

    $('#user1').on('click', function() {
        currentUser = QBUser1;
        connectToChat(QBUser1);
    });

    $('#user2').on('click', function() {
        currentUser = QBUser2;
        connectToChat(QBUser2);
    });*/
});

function connectToChat(user, opponent, message, flag) {
    $("#static").modal('show')

    QB.createSession({email: user.email, password: user.password}, function(err, res) {
        if (res) {
            token = res.token;
            user.id = res.user_id;

            mergeUsers([{user: user}]);

            QB.chat.connect({userId: user.id, password: user.password}, function(err, roster) {
                if (err) {
                    console.log(err);
                } else {
					$("#static").modal('hide')
					
					if(opponent != null)
						createNewDialog(opponent, message)
							
					if(flag == 0){
                        // setup scroll stickerpipe module
    					
                        setupStickerPipe();

                        retrieveChatDialogs();

                        // setup message listeners
                        setupAllListeners();

                        // setup scroll events handler
                        setupMsgScrollHandler();

                        setupStreamManagementListeners();
                    }
    					
                }
            });
        }
    });
}

function signup(user){
	QB.createSession(function(err, result) {
	  QB.users.create(user, function(err, user){
		  if (user) {
			// success
		  } else  {
			// error
		  }
		});
	});
}

function setupAllListeners() {
  QB.chat.onMessageListener         = onMessage;
  QB.chat.onSystemMessageListener   = onSystemMessageListener;
  QB.chat.onDeliveredStatusListener = onDeliveredStatusListener;
  QB.chat.onReadStatusListener      = onReadStatusListener;

  setupIsTypingHandler();
}
// reconnection listeners
function onDisconnectedListener(){
  console.log("onDisconnectedListener");
}

function onReconnectListener(){
  console.log("onReconnectListener");
}


// niceScroll() - ON
$(document).ready(
    function() {
        
    }
);
