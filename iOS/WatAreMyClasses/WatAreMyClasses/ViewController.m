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
    cache.userID=@"aj3roth";
    cache.token=@"mfGVvr3AJT9wMGYESuz5gwRcGnEwumrKTf27UARQ3MVIrOhuEnZa8llBDHL89w13";
    [cache doCache];

    // Do any additional setup after loading the view, typically from a nib.
}
-(void)doPathPolyline:(NSString *)to{
    WatService * svc=[WatService sharedService];
    [svc getClosestNodeWithLat:curLat lon:curLong completion:^(OVCResponse *resp, NSError *error) {//TODO: error handing.
        [svc getPathFromNode:((WatNode*)resp.result).ndid toNode:to completion:^(OVCResponse *resp, NSError *error) {
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

-(void) locationManager:(CLLocationManager*) manager didUpdateHeading:(nonnull CLHeading *)newHeading{
    [_mapView animateToBearing:newHeading.trueHeading];
}
-(void) locationManager:(CLLocationManager *)manager didUpdateLocations:(nonnull NSArray<CLLocation *> *)locations{
    CLLocation * loc=[locations lastObject];
    curLat=loc.coordinate.latitude;
    curLong=loc.coordinate.longitude;
    NSLog(@"Location Update: %f,%f",loc.coordinate.latitude,loc.coordinate.longitude);
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}
- (IBAction)unwindFromClasses:(UIStoryboardSegue *)unwindSegue
{
    NSString *bid=((ClassesViewController*)unwindSegue.sourceViewController).doneGoto;
    NSLog(@"Class: %@",bid);
    [self doPathPolyline:bid];
}
- (IBAction)unwindFromBuildings:(UIStoryboardSegue *)unwindSegue
{
    NSString * bid=((BuildingsViewController*)unwindSegue.sourceViewController).doneGoto;
    NSLog(@"Buildings: %@",bid);
    [self doPathPolyline:bid];
    
}

@end
