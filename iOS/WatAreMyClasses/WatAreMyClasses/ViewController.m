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
    
    GMSCameraPosition * camera = [GMSCameraPosition cameraWithLatitude:43.470366  longitude:-80.541945 zoom:18 bearing:0 viewingAngle:80]; // Setup our initial camera position over Waterloo.
    
    _mapView.settings.myLocationButton = TRUE; // Let users find themselves.
    _mapView.camera=camera; // Move to our initial camera.
    _mapView.myLocationEnabled=true; // Let users find themselves.
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
    cache.userID=@"aj3roth"; // Needs to be collected via QR code & stored in CacheManager, like in Android.
    cache.token=@"mfGVvr3AJT9wMGYESuz5gwRcGnEwumrKTf27UARQ3MVIrOhuEnZa8llBDHL89w13"; // Hey, that's mine ! :)
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

-(void) locationManager:(CLLocationManager*) manager didUpdateHeading:(nonnull CLHeading *)newHeading{
    [_mapView animateToBearing:newHeading.trueHeading]; // trueHeading is true north like Gmaps expects.
}
-(void) locationManager:(CLLocationManager *)manager didUpdateLocations:(nonnull NSArray<CLLocation *> *)locations{
    CLLocation * loc=[locations lastObject]; //Get most recent location.
    curLat=loc.coordinate.latitude; // Update for pathfinding.
    curLong=loc.coordinate.longitude;
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)unwindFromClasses:(UIStoryboardSegue *)unwindSegue // Callback from ClassesViewController
{
    NSString *bid=((ClassesViewController*)unwindSegue.sourceViewController).doneGoto; //NodeID for desired building
    NSLog(@"Class: %@",bid);
    [self doPathPolyline:bid];
}
- (IBAction)unwindFromBuildings:(UIStoryboardSegue *)unwindSegue// Callback from BuildingsViewController
{
    NSString * bid=((BuildingsViewController*)unwindSegue.sourceViewController).doneGoto; // NodeID for desired building
    NSLog(@"Buildings: %@",bid);
    [self doPathPolyline:bid];
    
}

@end
