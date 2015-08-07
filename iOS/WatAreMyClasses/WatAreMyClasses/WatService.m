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
NetworkManager *nm;
-(id) init{
    self=[super init];
    if (self){
        nm=[[NetworkManager alloc] initWithBaseURL:[NSURL URLWithString:@"http://ssvps.magmastone.net/"]];
        
    }
    return self;
}
- (void) getClosestNodeWithLat:(float) lat lon:(float) lon completion:(void (^) (OVCResponse *resp, NSError *error))complete {
    [nm GET:@"/getclosestnode" parameters:@{@"lat":[NSNumber numberWithFloat:lat],@"lon":[NSNumber numberWithFloat:lon]} completion:complete];
}

@end
