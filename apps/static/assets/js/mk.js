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

      initMaterialWizard: function() {
        // Code for the Validator
        var $validator = $('.card-wizard form').validate({
          rules: {
            firstname: {
              required: true,
              minlength: 3
            },
            lastname: {
              required: true,
              minlength: 3
            },
            email: {
              required: true,
              minlength: 3,
            }
          },
    
          highlight: function(element) {
            $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
          },
          success: function(element) {
            $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
          },
          errorPlacement: function(error, element) {
            $(element).append(error);
          }
        });
    
    
    
        // Wizard Initialization
        $('.card-wizard').bootstrapWizard({
          'tabClass': 'nav nav-pills',
          'nextSelector': '.btn-next',
          'previousSelector': '.btn-previous',
    
          onNext: function(tab, navigation, index) {
            var $valid = $('.card-wizard form').valid();
            if (!$valid) {
              $validator.focusInvalid();
              return false;
            }
          },
    
          onInit: function(tab, navigation, index) {
            //check number of tabs and fill the entire row
            var $total = navigation.find('li').length;
            var $wizard = navigation.closest('.card-wizard');
    
            $first_li = navigation.find('li:first-child a').html();
            $moving_div = $('<div class="moving-tab">' + $first_li + '</div>');
            $('.card-wizard .wizard-navigation').append($moving_div);
    
            refreshAnimation($wizard, index);
    
            $('.moving-tab').css('transition', 'transform 0s');
          },
    
          onTabClick: function(tab, navigation, index) {
            var $valid = $('.card-wizard form').valid();
    
            if (!$valid) {
              return false;
            } else {
              return true;
            }
          },
    
          onTabShow: function(tab, navigation, index) {
            var $total = navigation.find('li').length;
            var $current = index + 1;
    
            var $wizard = navigation.closest('.card-wizard');
    
            // If it's the last tab then hide the last button and show the finish instead
            if ($current >= $total) {
              $($wizard).find('.btn-next').hide();
              $($wizard).find('.btn-finish').show();
            } else {
              $($wizard).find('.btn-next').show();
              $($wizard).find('.btn-finish').hide();
            }
    
            button_text = navigation.find('li:nth-child(' + $current + ') a').html();
    
            setTimeout(function() {
              $('.moving-tab').text(button_text);
            }, 150);
    
            var checkbox = $('.footer-checkbox');
    
            if (!index == 0) {
              $(checkbox).css({
                'opacity': '0',
                'visibility': 'hidden',
                'position': 'absolute'
              });
            } else {
              $(checkbox).css({
                'opacity': '1',
                'visibility': 'visible'
              });
            }
    
            refreshAnimation($wizard, index);
          }
        });
    
    
        // Prepare the preview for profile picture
        $("#wizard-picture").change(function() {
          readURL(this);
        });
    
        $('[data-toggle="wizard-radio"]').click(function() {
          wizard = $(this).closest('.card-wizard');
          wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
          $(this).addClass('active');
          $(wizard).find('[type="radio"]').removeAttr('checked');
          $(this).find('[type="radio"]').attr('checked', 'true');
        });
    
        $('[data-toggle="wizard-checkbox"]').click(function() {
          if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).find('[type="checkbox"]').removeAttr('checked');
          } else {
            $(this).addClass('active');
            $(this).find('[type="checkbox"]').attr('checked', 'true');
          }
        });
    
        $('.set-full-height').css('height', 'auto');
    
        //Function to show image before upload
    
        function readURL(input) {
          if (input.files && input.files[0]) {
            var reader = new FileReader();
    
            reader.onload = function(e) {
              $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
            }
            reader.readAsDataURL(input.files[0]);
          }
        }
    
        $(window).resize(function() {
          $('.card-wizard').each(function() {
            $wizard = $(this);
    
            index = $wizard.bootstrapWizard('currentIndex');
            refreshAnimation($wizard, index);
    
            $('.moving-tab').css({
              'transition': 'transform 0s'
            });
          });
        });
    
        function refreshAnimation($wizard, index) {
          $total = $wizard.find('.nav li').length;
          $li_width = 100 / $total;
    
          total_steps = $wizard.find('.nav li').length;
          move_distance = $wizard.width() / total_steps;
          index_temp = index;
          vertical_level = 0;
    
          mobile_device = $(document).width() < 600 && $total > 3;
    
          if (mobile_device) {
            move_distance = $wizard.width() / 2;
            index_temp = index % 2;
            $li_width = 50;
          }
    
          $wizard.find('.nav li').css('width', $li_width + '%');
    
          step_width = move_distance;
          move_distance = move_distance * index_temp;
    
          $current = index + 1;
    
          if ($current == 1 || (mobile_device == true && (index % 2 == 0))) {
            move_distance -= 8;
          } else if ($current == total_steps || (mobile_device == true && (index % 2 == 1))) {
            move_distance += 8;
          }
    
          if (mobile_device) {
            vertical_level = parseInt(index / 2);
            vertical_level = vertical_level * 38;
          }
    
          $wizard.find('.moving-tab').css('width', step_width);
          $('.moving-tab').css({
            'transform': 'translate3d(' + move_distance + 'px, ' + vertical_level + 'px, 0)',
            'transition': 'all 0.5s cubic-bezier(0.29, 1.42, 0.79, 1)'
    
          });
        }
      },

      showSwal: function(type) {
        if (type == 'basic') {
          swal({
            title: "Here's a message!",
            type: 'success',
            buttonsStyling: false,
            confirmButtonClass: "btn btn-success"
          }).catch(swal.noop)
    
        } else if (type == 'title-and-text') {
          swal({
            title: "Here's a message!",
            text: "It's pretty, isn't it?",
            buttonsStyling: false,
            confirmButtonClass: "btn btn-info"
          }).catch(swal.noop)
    
        } else if (type == 'success-message') {
          swal({
            title: "Good job!",
            text: "You clicked the button!",
            buttonsStyling: false,
            confirmButtonClass: "btn btn-success",
            type: "success"
          }).catch(swal.noop)
    
        } else if (type == 'warning-message-and-confirmation') {
          swal({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-success',
            cancelButtonClass: 'btn btn-danger',
            confirmButtonText: 'Yes, delete it!',
            buttonsStyling: false
          })
          .then(function(result) {
            console.log(result)
            if(result.value) {
              swal({
                title: 'Deleted!',
                text: 'Your file has been deleted.',
                type: 'success',
                confirmButtonClass: "btn btn-success",
                buttonsStyling: false
              })
            }
            
          }).catch(swal.noop)
        } else if (type == 'warning-message-and-cancel') {
          swal({
            title: 'Are you sure?',
            text: 'You will not be able to recover this imaginary file!',
            type: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, keep it',
            confirmButtonClass: "btn btn-success",
            cancelButtonClass: "btn btn-danger",
            buttonsStyling: false
          }).then(function() {
            swal({
              title: 'Deleted!',
              text: 'Your imaginary file has been deleted.',
              type: 'success',
              confirmButtonClass: "btn btn-success",
              buttonsStyling: false
            }).catch(swal.noop)
          }, function(dismiss) {
            // dismiss can be 'overlay', 'cancel', 'close', 'esc', 'timer'
            if (dismiss === 'cancel') {
              swal({
                title: 'Cancelled',
                text: 'Your imaginary file is safe :)',
                type: 'error',
                confirmButtonClass: "btn btn-info",
                buttonsStyling: false
              }).catch(swal.noop)
            }
          })
    
        } else if (type == 'custom-html') {
          swal({
            title: 'HTML example',
            buttonsStyling: false,
            confirmButtonClass: "btn btn-success",
            html: 'You can use <b>bold text</b>, ' +
              '<a href="http://github.com">links</a> ' +
              'and other HTML tags'
          }).catch(swal.noop)
    
        } else if (type == 'auto-close') {
          swal({
            title: "Auto close alert!",
            text: "I will close in 2 seconds.",
            timer: 2000,
            showConfirmButton: false
          }).catch(swal.noop)
        } else if (type == 'input-field') {
          swal({
            title: 'Input something',
            html: '<div class="form-group">' +
              '<input id="input-field" type="text" class="form-control" />' +
              '</div>',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-success',
            cancelButtonClass: 'btn btn-danger',
            buttonsStyling: false
          }).then(function(result) {
            swal({
              type: 'success',
              html: 'You entered: <strong>' +
                $('#input-field').val() +
                '</strong>',
              confirmButtonClass: 'btn btn-success',
              buttonsStyling: false
    
            })
          }).catch(swal.noop)
        }
      },

      initDashboardPageCharts: function(summary) {
        // console.log(summary.replace(new RegExp("&"+"#"+"x27;", "g"), "'"));
        // console.log(JSON.parse(summary))
        summary = summary.replace(new RegExp("&"+"#"+"x27;", "g"), "'");
        summary = summary.replace(/'/g, '\"');
        // console.log(summary)
        summary = JSON.parse(summary)
        // console.log(summary[0])
        // console.log(JSON.parse("[" + summary + "]"))
        labels = []
        withdrawn = []
        deposited = []
        for (let i = 0; i < summary.length; i++) {
          // sum = .replace(new RegExp("&"+"#"+"x27;", "g"), "'");
          labels.push(i+1);
          withdrawn.push(summary[i][2]);
          deposited.push(summary[i][3]);
          console.log(summary[i]);
          // console.log(summary[i] + "<br>") ;
        }
        all_amount = withdrawn.concat(deposited)
        // console.log(all_amount)
        // console.log(Math.max(...all_amount))
        // console.log(Math.max(...deposited))
        // labels.push('test')
        // console.log(labels)
        if ($('#multipleBarsChart').length != 0 || $('#WithdrawnChart').length != 0 || $('#DepositedChart').length != 0) {

          /*  **************** Simple Bar Chart - barchart ******************** */

          var dataSimpleBarChart = {
            labels: labels,
            series: [
              withdrawn
            ]
          };

          var optionsSimpleBarChart = {
            seriesBarDistance: 10,
            high: Math.max(...withdrawn),
            axisX: {
              showGrid: false
            }, 
            axisY: {
              offset: 80,
              labelInterpolationFnc: function(value) {
                return Math.abs(value) > 999 ? Math.sign(value)*((Math.abs(value)/1000).toFixed(1)) + ' k' : Math.sign(value)*Math.abs(value)
              },
              scaleMinSpace: 15
            }
          };

          var responsiveOptionsSimpleBarChart = [
            ['screen and (max-width: 640px)', {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function(value) {
                  return value[0];
                }
              }
            }]
          ];

          var simpleBarChart = Chartist.Bar('#WithdrawnChart', dataSimpleBarChart, optionsSimpleBarChart, responsiveOptionsSimpleBarChart);

          //start animation for the Emails Subscription Chart
          md.startAnimationForBarChart(simpleBarChart);
            
          // /////////////////////////////// deposited /////////////////////

              var dataDepositedChart = {
                labels: labels,
                series: [
                  deposited
                ]
              };

              var optionsDepositedChart = {
                seriesBarDistance: 10,
                high: Math.max(...deposited),
                axisX: {
                  showGrid: false
                }, 
                axisY: {
                  offset: 80,
                  labelInterpolationFnc: function(value) {
                    return Math.abs(value) > 999 ? Math.sign(value)*((Math.abs(value)/1000).toFixed(1)) + ' k' : Math.sign(value)*Math.abs(value)
                  },
                  scaleMinSpace: 15
                }
              };

              var responsiveOptionsDepositedChart = [
                ['screen and (max-width: 640px)', {
                  seriesBarDistance: 5,
                  axisX: {
                    labelInterpolationFnc: function(value) {
                      return value[0];
                    }
                  }
                }]
              ];

              var depositedChart = Chartist.Bar('#DepositedChart', dataDepositedChart, optionsDepositedChart, responsiveOptionsDepositedChart);

              //start animation for the Emails Subscription Chart
              md.startAnimationForBarChart(depositedChart);

          // multiple bars
          var dataMultipleBarsChart = {
            labels: labels,
            series: [
              withdrawn,
              deposited
            ]
          };
    
          var optionsMultipleBarsChart = {
            seriesBarDistance: 10,
            // axisX: {
            //   showGrid: true
            // },
            // low: -10,
            high: Math.max(...all_amount),
            height: '20rem',
            // reverseData: true,
            // horizontalBars: true,
            axisX: {
              offset: 60
            },
            axisY: {
              offset: 80,
              labelInterpolationFnc: function(value) {
                return Math.abs(value) > 999 ? Math.sign(value)*((Math.abs(value)/1000).toFixed(1)) + ' k' : Math.sign(value)*Math.abs(value)
              },
              scaleMinSpace: 15
            }
            // stretch: true
          };
    
          var responsiveOptionsMultipleBarsChart = [
            ['screen and (max-width: 640px)', {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function(value) {
                  return value[0];
                }
              }
            }]
          ];
    
          var multipleBarsChart = Chartist.Bar('#multipleBarsChart', dataMultipleBarsChart, optionsMultipleBarsChart, responsiveOptionsMultipleBarsChart);
    
          //start animation for the Emails Subscription Chart
          mk.startAnimationForBarChart(multipleBarsChart);
        }
      },


      startAnimationForBarChart: function(chart) {

        chart.on('draw', function(data) {
          if (data.type === 'bar') {
            seq2++;
            data.element.animate({
              opacity: {
                begin: seq2 * delays2,
                dur: durations2,
                from: 0,
                to: 1,
                easing: 'ease'
              }
            });
          }
        });
    
        seq2 = 0;
      },
};