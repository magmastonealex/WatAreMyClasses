//
//  WelcomeViewController.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-12.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "WelcomeViewController.h"
#import <AVFoundation/AVFoundation.h>
#import <QRCodeReaderViewController/QRCodeReaderViewController.h>
#import "TokenStorage.h"
@interface WelcomeViewController ()
@property (nonatomic) QRCodeReaderViewController * reader;
@end

@implementation WelcomeViewController
- (void)viewDidLoad {
    [super viewDidLoad];
    
    // Do any additional setup after loading the view.
}
-(void)viewDidAppear:(BOOL)animated{
    [super viewDidAppear:animated];
    TokenStorage * stor = [TokenStorage sharedStorage];
    if(stor.userID != nil){// check to see if user has already logged in.
       // [self performSegueWithIdentifier:@"goNext" sender:self];
        
    
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}
- (IBAction)scanButton:(id)sender {
    NSArray *types = @[AVMetadataObjectTypeQRCode];
    _reader        = [QRCodeReaderViewController readerWithMetadataObjectTypes:types];
    
    // Set the presentation style
    _reader.modalPresentationStyle = UIModalPresentationFormSheet;
    
    // Using delegate methods
    _reader.delegate = self;
    
    
    [self presentViewController:_reader animated:YES completion:NULL];
}

- (void)reader:(QRCodeReaderViewController *)reader didScanResult:(NSString *)result
{
    [self dismissViewControllerAnimated:YES completion:^{
        NSLog(@"%@", result);
        NSArray * tokComponents=[result componentsSeparatedByString:@":"];
        TokenStorage * stor = [TokenStorage sharedStorage];
        [stor setUserID:[tokComponents objectAtIndex:0] withToken:[tokComponents objectAtIndex:1]];
        [self performSegueWithIdentifier:@"goNext" sender:self];
    }];
}

- (void)readerDidCancel:(QRCodeReaderViewController *)reader
{
    [self dismissViewControllerAnimated:YES completion:NULL];
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
