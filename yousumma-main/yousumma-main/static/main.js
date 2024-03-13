$(document).ready(function() {
    let player; 

    $('#transcriptForm').submit(function(event) {
        event.preventDefault(); 
        document.getElementById('spinner').style.display = 'block';
        
        var videoLink = $('#videoLink').val();

        if (!isValidYouTubeLink(videoLink)) {
            document.getElementById('spinner').style.display = 'none';
            alert('Error: Invalid YouTube link. Please enter a valid YouTube video link.');
            return;
        }
        
        $.ajax({
            type: 'POST',
            url: '/summarize',
            data: {video_link: videoLink},
            success: function(response) {
                document.getElementById('spinner').style.display = 'none';
                $('#summaryResult').show();
                
                // Clear previous results
                $('#summaryContent').empty();
                $('#transcriptContent').empty();
                
                // Update with new results
                $('#summaryContent').html(response.summary);
                $('#transcriptContent').html(response.transcript);
                
                // Destroy previous player instance if exists
                if (player) {
                    player.destroy();
                }

                // Initialize YouTube Player
                player = new YT.Player('player', {
                    height: '360',
                    width: '100%',
                    videoId: response.video_id,
                    playerVars: {
                        'autoplay': 1,
                        'controls': 1
                    },
                    events: {
                        'onReady': onPlayerReady
                    }
                });

                $('#player').css('display', 'block');

                
                // Scroll to the summary result section
                $('html, body').animate({
                    scrollTop: $('#summaryResult').offset().top
                }, 1000);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    // Switch between Summary and Transcript tabs
    $('#summaryTab').click(function() {
        $('#summaryTab').addClass('active');
        $('#transcriptTab').removeClass('active');
        $('#summaryContent').addClass('show active');
        $('#transcriptContent').removeClass('show active');
    });

    $('#transcriptTab').click(function() {
        $('#transcriptTab').addClass('active');
        $('#summaryTab').removeClass('active');
        $('#transcriptContent').addClass('show active');
        $('#summaryContent').removeClass('show active');
    });

    function onPlayerReady(event) {
        event.target.playVideo();
    }

    function isValidYouTubeLink(link) {
        return link.includes('youtu.be/') || link.includes('www.youtube.com/');
    }

});


function copyText() {
    var copyButton = document.getElementById("copyButton");
    var textToCopy = $('.tab-pane.active').text();

    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            console.log('Text copied successfully');

            copyButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check2-square" viewBox="0 0 16 16"> \
                <path d="M3 14.5A1.5 1.5 0 0 1 1.5 13V3A1.5 1.5 0 0 1 3 1.5h8a.5.5 0 0 1 0 1H3a.5.5 0 0 0-.5.5v10a.5.5 0 0 0 .5.5h10a.5.5 0 0 0 .5-.5V8a.5.5 0 0 1 1 0v5a1.5 1.5 0 0 1-1.5 1.5z"/> \
                <path d="m8.354 10.354 7-7a.5.5 0 0 0-.708-.708L8 9.293 5.354 6.646a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0"/> \
            </svg>';

            setTimeout(() => {
                copyButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16"> \
                    <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/> \
                </svg>';
            }, 2000); 
        })
        .catch(err => {
            console.error('Error copying text: ', err);
        });
}


function downloadText() {
    var textToDownload = $('.tab-pane.active').text();
    var videoLink = $('#videoLink').val();
    var blob = new Blob([textToDownload + '\n\nVideo Link: ' + videoLink], { type: "text/plain;charset=utf-8" });
    saveAs(blob, "summary.txt");
}

document.getElementById('inputLink').addEventListener('click', function(event) {
    event.preventDefault(); 
    document.getElementById('videoLink').focus();
});

$(document).ready(function() {
    $('html, body').animate({ scrollTop: 0 }, 'fast'); 
});

document.getElementById('but-submit').addEventListener('click', function(event){
    event.preventDefault(); 
    document.getElementById('but-submit').style.backgroundColor='#235789';

    setTimeout(function() {
        document.getElementById('but-submit').style.backgroundColor = '#235789';
    }, 3000); 
});

function downloadZip() {
    var zipFileUrl = '/download_extension';
    var filename = 'yousumma_chrm_extension.crx';
    
    fetch(zipFileUrl)
        .then(response => response.blob())
        .then(blob => saveAs(blob, filename))
        .catch(error => console.error('Error downloading file:', error));
}