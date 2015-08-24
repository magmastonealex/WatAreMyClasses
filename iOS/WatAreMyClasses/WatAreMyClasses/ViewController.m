//
//  ViewController.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "ViewController.h"
#import "DataCacher.h"
#import "ClassesViewController.h"
#import "BuildingsViewController.h"
#import "WatNode.h"
#import "TokenStorage.h"
@import GoogleMaps;
@interface ViewController ()
@property (weak, nonatomic) IBOutlet GMSMapView *mapView;

@end

@implementation ViewController
CLLocationManager * locationmanager;
GMSPolyline * pLine;
double curLat;
double curLong;


- (void)viewDidLoad {
    [super viewDidLoad];
    
    GMSCameraPosition * camera = [GMSCameraPosition cameraWithLatitude:43.470366  longitude:-80.541945 zoom:18 bearing:0 viewingAngle:80]; // Setup our initial camera position over Waterloo.
    
    _mapView.settings.myLocationButton = FALSE; // Let users find themselves.
    _mapView.camera=camera; // Move to our initial camera.
    _mapView.myLocationEnabled=true; // Let users find themselves.
    _mapView.settings.indoorPicker=false;
    if(locationmanager==nil){ // Probably yes, but not always.
        locationmanager = [[CLLocationManager alloc] init]; // Make a new LocationManager so that we can get location info.
    }

    [locationmanager requestWhenInUseAuthorization]; // New in iOS 8
    locationmanager.delegate=self; // We want to hear about location & orientation updates.
    locationmanager.desiredAccuracy=kCLLocationAccuracyBest; // We're doing path-based navigation. Need high accuracy.
    locationmanager.distanceFilter=1; // If user moves more than 1 metre, call our delegate method.
    
    [locationmanager startUpdatingLocation];
    [locationmanager startUpdatingHeading];
    
    DataCacher * cache=[DataCacher sharedCache]; // Singleton to cache web-based data
    TokenStorage *tStore=[TokenStorage sharedStorage];
    cache.userID=tStore.userID;
    cache.token=tStore.token;
    NSLog(@"Using userID: %@", cache.userID);
    [cache doCache]; // Prepare the cache for when a view-controller needs it later.

    // Do any additional setup after loading the view, typically from a nib.
}
//Draw a Polyline on the map, removing the previous one. Uses user's last-known location.
-(void)doPathPolyline:(NSString *)to{
    WatService * svc=[WatService sharedService]; // Another singleton. Making these is very expensive on iOS.
    [svc getClosestNodeWithLat:curLat lon:curLong completion:^(OVCResponse *resp, NSError *error) {//TODO: error handing.
        [svc getPathFromNode:((WatNode*)resp.result).ndid toNode:to completion:^(OVCResponse *resp, NSError *error) { //TODO: Error handling.
            GMSMutablePath*gmp = [GMSMutablePath path];
            for (WatNode*nde in resp.result) {
                NSLog(@"Path along: %@",nde.ndid);
                [gmp addCoordinate:CLLocationCoordinate2DMake([nde.lat doubleValue], [nde.lon doubleValue])];
            }
            if(pLine){
                pLine.map = nil;
            }
            pLine=[GMSPolyline polylineWithPath:gmp];
            pLine.strokeColor=[UIColor redColor];
            pLine.strokeWidth=3.0f;
            pLine.map=_mapView;
        }];
    }];
}
int cnt=0;
-(void) locationManager:(CLLocationManager*) manager didUpdateHeading:(nonnull CLHeading *)newHeading{
    if(cnt > 10){
        [_mapView animateToBearing:newHeading.trueHeading]; // trueHeading is true north like Gmaps expects.
        cnt=0;
    }else{
        cnt++;
    }
    }
-(void) locationManager:(CLLocationManager *)manager didUpdateLocations:(nonnull NSArray<CLLocation *> *)locations{
    CLLocation * loc=[locations lastObject]; //Get most recent location.
    curLat=loc.coordinate.latitude; // Update for pathfinding.
    curLong=loc.coordinate.longitude;
    [_mapView animateToLocation:loc.coordinate];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)unwindFromClasses:(UIStoryboardSegue *)unwindSegue // Callback from ClassesViewController
{
    NSString *bid=((ClassesViewController*)unwindSegue.sourceViewController).doneGoto; //NodeID for desired building
    NSLog(@"Class: %@",bid);
    if([bid isEqualToString:@"none"]){
        UIAlertController *alertController = [UIAlertController
                                              alertControllerWithTitle:@"Make sure to sign in!"
                                              message:@"You need to sign in to view your classes!"
                                              preferredStyle:UIAlertControllerStyleAlert];
        UIAlertAction *cancelAction = [UIAlertAction
                                       actionWithTitle:@"Go back"
                                       style:UIAlertActionStyleCancel
                                       handler:^(UIAlertAction *action)
                                       {
                                           NSLog(@"Cancelled");
                                       }];
        
        UIAlertAction *okAction = [UIAlertAction
                                   actionWithTitle:@"Sign In"
                                   style:UIAlertActionStyleDefault
                                   handler:^(UIAlertAction *action)
                                   {
                                       [self performSegueWithIdentifier:@"gotoLogin" sender:self];

                                   }];
        [alertController addAction:cancelAction];
        [alertController addAction:okAction];
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            [self presentViewController:alertController animated:YES completion:nil];
        });
    }else{
    [self doPathPolyline:bid];
    }
}
- (IBAction)unwindFromBuildings:(UIStoryboardSegue *)unwindSegue// Callback from BuildingsViewController
{
    NSString * bid=((BuildingsViewController*)unwindSegue.sourceViewController).doneGoto; // NodeID for desired building
    NSLog(@"Buildings: %@",bid);
    if([bid isEqualToString:@"none"]){
        UIAlertController *alertController = [UIAlertController
                                              alertControllerWithTitle:@"Internet connection required!"
                                              message:@"You need an internet connection to use this app!"
                                              preferredStyle:UIAlertControllerStyleAlert];
        UIAlertAction *cancelAction = [UIAlertAction
                                       actionWithTitle:@"OK"
                                       style:UIAlertActionStyleDefault
                                       handler:^(UIAlertAction *action)
                                       {
                                           DataCacher * cache=[DataCacher sharedCache];
                                           [cache doCache];
                                           NSLog(@"Cancelled");
                                       }];
        [alertController addAction:cancelAction];
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            [self presentViewController:alertController animated:YES completion:nil];
        });
    }else{
        [self doPathPolyline:bid];
    }
}

@end
