// War gestern kurz vor knapp drum etwas chaotisch,
//
// hab nochmal eine aufgeräumte Version inkl. der Msg detection.
// Ist fast das gleiche was dein Code macht, kannst ja mal reinschauen.
// Der ST verhält sich bei Serial sehr unterschiedlich zum NXP,
// der hat nämlich 16 Byte RX Buffer in Hardware und hängt sich auch nicht weg,
// wenn die nicht sofort abgeholt werden. Da hast Du recht, dass der ST etwas speziell reagiert.
//
//
// Für das Schreiben von Serial in die Structs könnte „Union“ noch interessant sein,
// Benutz Du ja eh schon, wenn man da noch ein Byte Array drüber packt,
// spart man sich den „Memcopy“. Man kann dann den Serial Buffer direkt Byte für Byte über die Struct  schreiben.
//
//
//
// Grüße
// Sebastian
//
//
//
//
//
// union receive_msg{
//     MassageIn  MSG_in;
//     uint8_t  MSG_byte[8];
// }MSG_rx ;
//
//
//
// MSG_rx.MSG_byte[i] =  input_buffer[pos_read + i];
//
//
// #include "mbed.h"
//
//
//
// //Serial pc(SERIAL_TX, SERIAL_RX, 115200); // tx, rx
// Serial pc(USBTX, USBRX, 115200); // tx, rx
// DigitalOut led(LED1);
//
// #define massage_length 12
// #define buffer_size    massage_length * 2
// #define start_byte     0xFE
// #define end_byte       0x0F
//
// char input_buffer[buffer_size];
// int pos_write  = 0;
// int pos_read   = 0;
// bool msg_frame = 0;
// char massage[massage_length];
//
// void rx_input(){
//     input_buffer[pos_write]= pc.getc();
//
//     //overrun protect if Msg handle is to slow
//     if (pos_write < buffer_size) {
//         pos_write++;
//     }
// }
//
//
// int main() {
//     pc.printf("Wait for input events\r\n");
//     pc.attach(&rx_input);
//     while(1) {
//         // new Byte rx
//         while(pos_read < pos_write) {
//
//             if(msg_frame) {
//                 // full Msg detected
//
//                 // handle Msg
//                 pos_write = 0;
//                 for (int i=1; (i < massage_length); i++) {
//                     pc.printf("%c\r\n", input_buffer[pos_read + i]);
//                     massage[i]= input_buffer[pos_read + i];
//                 }
//                 // clear Frame (prevent wrong det)
//                 input_buffer[pos_read] = 0x00;
//                 // clear Frame (prevent wrong det)
//                 input_buffer[pos_read + massage_length] = 0x00;
//                 // reset flag
//                 msg_frame = false;
//                 // reset read Pos
//                 pos_read  = 0;
//             } else {
//                 // not a full message
//
//                 // Search Start Byte
//                 if (input_buffer[pos_read] != start_byte) {
//                     if (pos_read > (buffer_size - massage_length)) {
//                         // If Out auf Input Buffer
//
//                         // reset Buffer
//                         pos_write = 0;
//                         pos_read  = 0;
//                     } else
//                         // search go on
//                         pos_read++;
//                 } else {
//                     // Start Byte detected
//
//                     // Search End Byte
//                     if (input_buffer[pos_read + massage_length] == end_byte) {
//                         // Msg rec
//                         msg_frame = true;
//                     } else {
//                         // Start without End go on
//                         pos_read++;
//                     }
//                 }
//             }
//         }
//
//         wait(0.5);
//         led = !led;
//         }
//  }
