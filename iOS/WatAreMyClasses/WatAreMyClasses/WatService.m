//
//  WatService.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "WatService.h"
#import "WatNode.h"
#import "WatClass.h"
#import "WatBuilding.h"
#import "NetworkManager.h"
@implementation WatService
 // This is our abstractor class.
@synthesize nm;
+ (id)sharedService {
    static WatService *sharedService = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedService = [[self alloc] init];
    });
    return sharedService;
}
-(id) init{
    self=[super init];
    if (self){
        nm=[[NetworkManager alloc] initWithBaseURL:[NSURL URLWithString:@"http://ssvps.magmastone.net"]]; // Init with API endpoint.
        
    }
    return self;
}

//Get closest WatNode to the user.
- (void) getClosestNodeWithLat:(double) lat lon:(double) lon completion:(void (^) (OVCResponse *resp, NSError *error))complete {
    [nm GET:@"/getclosestnode" parameters:@{@"lat":[[NSNumber numberWithDouble:lat] stringValue],@"lon":[[NSNumber numberWithDouble:lon] stringValue]} completion:complete];
}

//Get a path between two given NodeIDs. Returns an NSArray of WatNodes.
-(void) getPathFromNode:(NSString*)node1 toNode:(NSString*)node2 completion:(void (^) (OVCResponse *resp, NSError *error))complete {
    [nm GET:@"/getpath" parameters:@{@"node1":node1,@"node2":node2} completion:complete];
}

//Get schedule for a given UserID and token. Get those values from the QR code. Returns an NSArray of WatClasses.
-(void)getScheduleforUser:(NSString*)userID andToken:(NSString*)token completion:(void (^) (OVCResponse *resp, NSError *error))complete{
    [nm GET:@"/getschedule" parameters:@{@"userid":userID,@"token":token} completion:complete];
}

//Get user's next class. Pass userID and token from QR code. Returns a WatClass.
-(void)getNextClassForUser:(NSString*)userID andToken:(NSString*)token completion:(void (^) (OVCResponse *resp, NSError *error))complete{
    [nm GET:@"/getnextclass" parameters:@{@"userid":userID,@"token":token} completion:complete];
}

//Get list of all buildings. Should be cached client and server-side.
-(void)getBuildings:(void (^) (OVCResponse *resp, NSError *error))complete{
    [nm GET:@"/buildinglist" parameters:nil completion:complete];
}

@end
