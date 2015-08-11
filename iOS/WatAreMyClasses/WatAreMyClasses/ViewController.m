//
//  ViewController.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "ViewController.h"
#import "DataCacher.h"
@import GoogleMaps;
@interface ViewController ()
@property (weak, nonatomic) IBOutlet GMSMapView *mapView;

@end

@implementation ViewController
CLLocationManager * locationmanager;
- (void)viewDidLoad {
    [super viewDidLoad];
    //AlzaSyANOLtR9yMGFcquqC0M6BvlUMTmgLUwoX4
    //
    GMSCameraPosition * camera = [GMSCameraPosition cameraWithLatitude:43.470366  longitude:-80.541945 zoom:18 bearing:0 viewingAngle:80];
    
    _mapView.settings.myLocationButton = TRUE;
    _mapView.camera=camera;
    _mapView.myLocationEnabled=true;
    if(locationmanager==nil){
        locationmanager = [[CLLocationManager alloc] init];
    }
    [locationmanager requestWhenInUseAuthorization];
    locationmanager.delegate=self;
    locationmanager.desiredAccuracy=kCLLocationAccuracyBest;
    locationmanager.distanceFilter=1;
    [locationmanager startUpdatingLocation];
    [locationmanager startUpdatingHeading];
    
    DataCacher * cache=[DataCacher sharedCache];
    [cache doCache];
    // Do any additional setup after loading the view, typically from a nib.
}
-(void) locationManager:(CLLocationManager*) manager didUpdateHeading:(nonnull CLHeading *)newHeading{
    [_mapView animateToBearing:newHeading.trueHeading];
}
-(void) locationManager:(CLLocationManager *)manager didUpdateLocations:(nonnull NSArray<CLLocation *> *)locations{
    CLLocation * loc=[locations lastObject];
    NSLog(@"Location Update: %f,%f",loc.coordinate.latitude,loc.coordinate.longitude);
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}
- (IBAction)classesClicked:(id)sender {
}
- (IBAction)buildingsClicked:(id)sender {
}

@end
