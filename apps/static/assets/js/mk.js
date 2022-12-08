mk = {

    showNotification: function(from, align, type, msg) {
        // type = ['', 'info', 'danger', 'success', 'warning', 'rose', 'primary'];
    
        // color = Math.floor((Math.random() * 6) + 1);
    
        $.notify({
          icon: "add_alert",
          message: msg
    
        }, {
          type: type,
          timer: 3000,
          placement: {
            from: from,
            align: align
          }
        });
      },
};