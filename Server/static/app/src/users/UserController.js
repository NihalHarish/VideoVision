  (function(){

    angular
    .module('users')
    .controller('UserController', [ "$scope", "$http", "$compile", "$httpParamSerializerJQLike",
      UserController
      ]);

  /**
   * Main Controller for the Angular Material Starter App
   * @param $scope
   * @param $mdSidenav
   * @param avatarsService
   * @constructor
   */
   function UserController($scope, $http, $compile) {
    $scope.getSearchResults = function() {
      var searchQuery = $scope.queryText;

      requestResults(searchQuery, dataRecieved);
    };

    function dataRecieved(data) {
      // gotta construct a new card and append it into the dom dynamically. Use the code in "dataNotRecieved" as an example.
      
      alert("Success!");
    };

    function requestResults(query, callback) {
/*      $http({
        url: 'http://localhost:8000', 
        method: "GET",
        params: {query: query}
      })
      .success(callback)
      .error(dataNotRecieved);

      var post_data =  {"statements":[{"statement":"MATCH (v:Video) RETURN v ",
      "resultDataContents":["graph"]}]};*/
    


      $http({
        url: "http://localhost:5000/nodeQuery",
        method: "POST",
        data: encodeURI(query),
        headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
      }).success(callback)
      .error(function (data) {
        console.log(data);
      });
    }

    $scope.playVideo = function(){

      var video_player = document.getElementById("v_player");
      if(playSwitch){
        video_player.play();
      }
      else
        video_player.pause();
      playSwitch = !playSwitch;      
      
    }

    $scope.startVideo = function(){

      var video_player = document.getElementById("v_player");
      video_player.innerHTML = '<source src='+currentVideo["video"]+'.mp4 type="video/mp4">'
      video_player.currentTime = (currentVideo["start"]/30);
      video_player.addEventListener('timeupdate', function() {
        if(this.currentTime > currentVideo["end"]/30){
          this.pause();
        }
      });
      video_player.play();
      playSwitch = false;

    }

    

    $scope.nextVideo = function(){
      var video_player = document.getElementById("v_player");
      video_player.pause();      
      currentVideo = videoPlaylist[(++currentVideoIndex)%videoPlaylist.length];
      // video_player.innerHTML = '<source src="'+currentVideo["video"]+'.mp4" type="video/mp4">';
      video_player.innerHTML = '<source src="movie1.mp4" type="video/mp4">';
      video_player.load();
      alert("nextVideo");
    }

    $scope.prevVideo = function(){
      var video_player = document.getElementById("v_player");
      video_player.pause();

      currentVideo = videoPlaylist[(--currentVideoIndex)%1];
      video_player.innerHTML = '<source src='+currentVideo["video"]+'.mp4 type="video/mp4">';
      video_player.load();

    }



    function parseJSON(data){
      videoPlaylist = [];
      currentVideo  = {};
      currentVideoIndex = 0
      for (var i = 0; i < data.length; i++){
        videoObject = data[i];
        videoPlaylist.push(videoObject);
        
      }
      currentVideo = videoPlaylist[0];
    }




    function dataNotRecieved(data) {
        /*var str = '<md-card class="md-whiteframe-2dp">\
          <md-card-title>\
            <md-card-title-text>\
              <span class="md-headline">Random Title</span>\
              <span class="md-subhead">SELECT * FROM VIRAT;</span>\
            </md-card-title-text>\
          </md-card-title>\
          <md-card-actions layout="row" layout-align="end center">\
            <md-button class="md-raised md-primary">BUTTON 1</md-button>\
            <md-button>BUTTON 2</md-button>\
          </md-card-actions>\
          </md-card>';*/
          // var mod = '[{"video": "VIRAT_S_010203_10_001092_001121",  "node": "11",  "start": 300, "end": 620}, {"video" : "VIRAT_S_010203_10_001092_001121", "node" :"12", "start": 300, "end": 620}]';
          var j = '{"VIRAT_S_010203_10_001092_001121": {"objects": {"11": [{"start": 300, "end": 620}], "12": [{"start": 300, "end": 620}]}}}';
          var mod = '[{"video": "VIRAT_S_010203_10_001092_001121",  "node": "11",  "start": 300, "end": 620}, {"video" : "movie1", "node" :"12", "start": 300, "end": 620}]';
          video_json = JSON.parse(mod);
          
          parseJSON(video_json);






          var str = '<md-card>\
          <md-card-title>\
          <md-card-title-text>\
          <span class="md-headline">Card with  image</span>\
          <span class="md-subhead">Extra Large</span>\
          </md-card-title-text>\
          </md-card-title>\
          <md-card-content layout="row" layout-align="space-between">\
          <video id="v_player" width="720" height="480">\
          </video>\
          <svg width="100%" height="100%" pointer-events="all"><line class="link" x1="389.9882256788036" stroke="#999" y1="205.77834714189285" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="166.0299282582989" stroke="#999" y1="386.01074170761" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="629.9189091918289" stroke="#999" y1="382.33290765739247" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="235.2331761792317" stroke="#999" y1="549.7314808094781" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="162.39099760579052" stroke="#999" y1="344.1711479859698" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="213.07037453192578" stroke="#999" y1="319.3449407312118" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="213.07037453192578" stroke="#999" y1="319.3449407312118" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="615.9346078629752" stroke="#999" y1="457.76273340459056" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="422.8500316489297" stroke="#999" y1="209.57745078271654" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="532.879610955678" stroke="#999" y1="491.0028193638629" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="532.879610955678" stroke="#999" y1="491.0028193638629" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="438.535519028529" stroke="#999" y1="279.27206703776557" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="438.535519028529" stroke="#999" y1="279.27206703776557" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="359.417910097508" stroke="#999" y1="422.5247004759209" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="359.417910097508" stroke="#999" y1="422.5247004759209" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="507.8061144677822" stroke="#999" y1="286.6911833983939" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="613.0608357230933" stroke="#999" y1="353.215988867733" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="209.55863532543995" stroke="#999" y1="519.2356771402749" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="414.6271865952398" stroke="#999" y1="263.0435111797576" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="414.6271865952398" stroke="#999" y1="263.0435111797576" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="470.285297285568" stroke="#999" y1="617.1373381364776" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="242.90286597690113" stroke="#999" y1="520.8276131890365" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="522.9270401101573" stroke="#999" y1="583.2541357036669" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="439.93661543135556" stroke="#999" y1="613.6707895641215" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="526.8862455126759" stroke="#999" y1="341.13352309733085" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="526.8862455126759" stroke="#999" y1="341.13352309733085" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="180.016765524963" stroke="#999" y1="306.66152210724414" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="501.7919064328629" stroke="#999" y1="606.138332478628" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="475.0658169110151" stroke="#999" y1="579.4282977579" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="475.0658169110151" stroke="#999" y1="579.4282977579" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="490.05074625238444" stroke="#999" y1="333.5281305708165" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="490.05074625238444" stroke="#999" y1="333.5281305708165" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="266.76722856409157" stroke="#999" y1="556.5730432663089" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="635.9258197908348" stroke="#999" y1="421.49641821543037" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="405.8931921955255" stroke="#999" y1="404.90696986223054" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="405.8931921955255" stroke="#999" y1="404.90696986223054" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="405.8931921955255" stroke="#999" y1="404.90696986223054" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="405.8931921955255" stroke="#999" y1="404.90696986223054" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="327.1280622822082" stroke="#999" y1="321.3379012746402" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="327.1280622822082" stroke="#999" y1="321.3379012746402" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="480.6089633637976" stroke="#999" y1="279.50761176555943" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="218.1880116675096" stroke="#999" y1="282.5961574850597" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="356.1435302573995" stroke="#999" y1="210.1601935415805" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="414.16746918040434" stroke="#999" y1="597.6175388432819" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="308.52302038115806" stroke="#999" y1="369.86446742049696" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="308.52302038115806" stroke="#999" y1="369.86446742049696" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="326.9769955198293" stroke="#999" y1="236.15097911357333" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="317.54090112413894" stroke="#999" y1="407.06266995635144" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="317.54090112413894" stroke="#999" y1="407.06266995635144" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="317.54090112413894" stroke="#999" y1="407.06266995635144" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="317.54090112413894" stroke="#999" y1="407.06266995635144" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="295.68147749664206" stroke="#999" y1="551.1993757959791" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="511.70968656651354" stroke="#999" y1="359.41615960169844" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="511.70968656651354" stroke="#999" y1="359.41615960169844" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="364.7780646485856" stroke="#999" y1="245.86131133432005" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="364.7780646485856" stroke="#999" y1="245.86131133432005" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="464.4397475753218" stroke="#999" y1="332.08424841906066" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="464.4397475753218" stroke="#999" y1="332.08424841906066" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="464.4397475753218" stroke="#999" y1="332.08424841906066" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="464.4397475753218" stroke="#999" y1="332.08424841906066" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="464.4397475753218" stroke="#999" y1="332.08424841906066" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="532.6143615896572" stroke="#999" y1="555.1364161937563" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="340.12567462039704" stroke="#999" y1="387.524618846807" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="340.12567462039704" stroke="#999" y1="387.524618846807" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="207.54987101337994" stroke="#999" y1="487.7439982624544" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="193.87240526509007" stroke="#999" y1="358.3758637042414" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="193.87240526509007" stroke="#999" y1="358.3758637042414" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="430.23678587056037" stroke="#999" y1="418.90611271239646" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="430.23678587056037" stroke="#999" y1="418.90611271239646" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="603.3696369663195" stroke="#999" y1="415.45851978725557" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="603.3696369663195" stroke="#999" y1="415.45851978725557" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="494.06136183291284" stroke="#999" y1="383.76980164185125" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="494.06136183291284" stroke="#999" y1="383.76980164185125" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="494.06136183291284" stroke="#999" y1="383.76980164185125" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="334.84554294323044" stroke="#999" y1="364.5767373024954" x2="390.9655547644213" y2="306.96853510974034"></line><line class="link" x1="334.84554294323044" stroke="#999" y1="364.5767373024954" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="334.84554294323044" stroke="#999" y1="364.5767373024954" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="334.84554294323044" stroke="#999" y1="364.5767373024954" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="421.82823893039483" stroke="#999" y1="470.9441459363523" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="421.82823893039483" stroke="#999" y1="470.9441459363523" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="421.82823893039483" stroke="#999" y1="470.9441459363523" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="363.77901888606254" stroke="#999" y1="530.572000801557" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="363.77901888606254" stroke="#999" y1="530.572000801557" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="483.20391357117467" stroke="#999" y1="439.55166314571574" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="483.20391357117467" stroke="#999" y1="439.55166314571574" x2="540.0052677675802" y2="409.25045682438923"></line><line class="link" x1="483.20391357117467" stroke="#999" y1="439.55166314571574" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="234.79125731809722" stroke="#999" y1="419.3291572286286" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="234.79125731809722" stroke="#999" y1="419.3291572286286" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="234.79125731809722" stroke="#999" y1="419.3291572286286" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="464.4332992199693" stroke="#999" y1="254.47792238912564" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="345.14995956235623" stroke="#999" y1="466.1286925047719" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="345.14995956235623" stroke="#999" y1="466.1286925047719" x2="257.4645076834816" y2="366.21637061108754"></line><line class="link" x1="452.81647849805927" stroke="#999" y1="447.2249116639056" x2="452.3802660477854" y2="523.3031755039692"></line><line class="link" x1="452.81647849805927" stroke="#999" y1="447.2249116639056" x2="421.54941954814166" y2="351.7545552192498"></line><line class="link" x1="219.8440502996758" stroke="#999" y1="437.2174940806786" x2="291.5324524408546" y2="467.0256825241999"></line><line class="link" x1="219.8440502996758" stroke="#999" y1="437.2174940806786" x2="257.4645076834816" y2="366.21637061108754"></line><circle class="node gpe" r="10" fill="#E81042" cx="389.9882256788036" cy="205.77834714189285"><title>Arizona</title></circle><circle class="node doc" r="10" cx="390.9655547644213" cy="306.96853510974034"><title>broke</title></circle><circle class="node doc" r="10" cx="257.4645076834816" cy="366.21637061108754"><title>fraudulent</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="166.0299282582989" cy="386.01074170761"><title>Colorado</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="629.9189091918289" cy="382.33290765739247"><title>Connecticut</title></circle><circle class="node doc" r="10" cx="540.0052677675802" cy="409.25045682438923"><title>pennywise</title></circle><circle class="node doc" r="10" cx="291.5324524408546" cy="467.0256825241999"><title>startup</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="235.2331761792317" cy="549.7314808094781"><title>Georgia</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="162.39099760579052" cy="344.1711479859698"><title>Hawaii</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="213.07037453192578" cy="319.3449407312118"><title>Idaho</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="615.9346078629752" cy="457.76273340459056"><title>Iowa</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="422.8500316489297" cy="209.57745078271654"><title>Louisiana</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="532.879610955678" cy="491.0028193638629"><title>Maine</title></circle><circle class="node doc" r="10" cx="452.3802660477854" cy="523.3031755039692"><title>sold</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="438.535519028529" cy="279.27206703776557"><title>Minnesota</title></circle><circle class="node doc" r="10" cx="421.54941954814166" cy="351.7545552192498"><title>fortune_100</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="359.417910097508" cy="422.5247004759209"><title>Mississippi</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="507.8061144677822" cy="286.6911833983939"><title>Nevada</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="613.0608357230933" cy="353.215988867733"><title>Ohio</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="209.55863532543995" cy="519.2356771402749"><title>Oklahoma</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="414.6271865952398" cy="263.0435111797576"><title>Texas</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="470.285297285568" cy="617.1373381364776"><title>Utah</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="242.90286597690113" cy="520.8276131890365"><title>Washington</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="522.9270401101573" cy="583.2541357036669"><title>Wisconsin</title></circle><circle class="node gpe" r="10" fill="#E81042" cx="439.93661543135556" cy="613.6707895641215"><title>Wyoming</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="526.8862455126759" cy="341.13352309733085"><title>Nokia</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="180.016765524963" cy="306.66152210724414"><title>Audi</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="501.7919064328629" cy="606.138332478628"><title>PizzaHut</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="475.0658169110151" cy="579.4282977579"><title>Apple</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="490.05074625238444" cy="333.5281305708165"><title>General_Motors</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="266.76722856409157" cy="556.5730432663089"><title>Ford_Motor</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="635.9258197908348" cy="421.49641821543037"><title>Airtel</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="405.8931921955255" cy="404.90696986223054"><title>Morgan_Stanley</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="327.1280622822082" cy="321.3379012746402"><title>Bloomberg</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="480.6089633637976" cy="279.50761176555943"><title>JP_Morgan</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="218.1880116675096" cy="282.5961574850597"><title>FedEx</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="356.1435302573995" cy="210.1601935415805"><title>Bank_of_America</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="414.16746918040434" cy="597.6175388432819"><title>Cardinal_Health</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="308.52302038115806" cy="369.86446742049696"><title>IBM</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="326.9769955198293" cy="236.15097911357333"><title>Kroger</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="317.54090112413894" cy="407.06266995635144"><title>Puma</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="295.68147749664206" cy="551.1993757959791"><title>Wells_Fargo</title></circle><circle class="node org" r="10" fill="#10DDE8" cx="511.70968656651354" cy="359.41615960169844"><title>Boeing</title></circle><circle class="node person" r="10" fill="#80e810" cx="364.7780646485856" cy="245.86131133432005"><title>Sirena_Trombly</title></circle><circle class="node person" r="10" fill="#80e810" cx="464.4397475753218" cy="332.08424841906066"><title>Larraine_Mahlum</title></circle><circle class="node person" r="10" fill="#80e810" cx="532.6143615896572" cy="555.1364161937563"><title>Jeanelle_Munyon</title></circle><circle class="node person" r="10" fill="#80e810" cx="340.12567462039704" cy="387.524618846807"><title>Franchesca_Dulmage</title></circle><circle class="node person" r="10" fill="#80e810" cx="207.54987101337994" cy="487.7439982624544"><title>Chassidy_Chico</title></circle><circle class="node person" r="10" fill="#80e810" cx="193.87240526509007" cy="358.3758637042414"><title>Marilyn_Philson</title></circle><circle class="node person" r="10" fill="#80e810" cx="430.23678587056037" cy="418.90611271239646"><title>Stephaine_Jeremiah</title></circle><circle class="node person" r="10" fill="#80e810" cx="603.3696369663195" cy="415.45851978725557"><title>Alvaro_Stanek</title></circle><circle class="node person" r="10" fill="#80e810" cx="494.06136183291284" cy="383.76980164185125"><title>Andreas_Roundy</title></circle><circle class="node person" r="10" fill="#80e810" cx="334.84554294323044" cy="364.5767373024954"><title>Marcella_Eberhart</title></circle><circle class="node person" r="10" fill="#80e810" cx="421.82823893039483" cy="470.9441459363523"><title>Anthony_Even</title></circle><circle class="node person" r="10" fill="#80e810" cx="363.77901888606254" cy="530.572000801557"><title>Shin_Fishback</title></circle><circle class="node person" r="10" fill="#80e810" cx="483.20391357117467" cy="439.55166314571574"><title>Shyla_Chu</title></circle><circle class="node person" r="10" fill="#80e810" cx="234.79125731809722" cy="419.3291572286286"><title>Daniella_Surratt</title></circle><circle class="node person" r="10" fill="#80e810" cx="464.4332992199693" cy="254.47792238912564"><title>Alina_Vidal</title></circle><circle class="node person" r="10" fill="#80e810" cx="345.14995956235623" cy="466.1286925047719"><title>Elia_Silveria</title></circle><circle class="node person" r="10" fill="#80e810" cx="452.81647849805927" cy="447.2249116639056"><title>Doug_Weisbrod</title></circle><circle class="node person" r="10" fill="#80e810" cx="219.8440502996758" cy="437.2174940806786"><title>Billye_Hitchings</title></circle></svg>\
          <section layout="row" layout-sm="column" layout-align="center center" layout-wrap>\
          <md-button class="md-raised" ng-click="startVideo();">Start</md-button>\
          <md-button class="md-raised md-primary" ng-click="playVideo();">Play/Pause</md-button>\
          <md-button class="md-raised md-warn" ng-click="nextVideo();">Next</md-button>\
          <md-button class="md-raised md-warn"    ng-click="prevVideo();">Reset</md-button>\
          <div class="label"></div>\
          </section>\
          </md-button>\
          </md-card-actions>\
          </md-card-content>\
          </md-card>';
          var st = document.getElementById('resultDisplay');
          st.innerHTML =  str;
          playSwitch = true;
          $compile(st)($scope);
        }
      }



    })();

// <div class="md-media-xl card-media"></div>\