//
//  WatService.h
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Overcoat/Overcoat.h>
#import "NetworkManager.h"
@interface WatService : NSObject
@property (nonatomic) NetworkManager *nm;
+ (id)sharedService;
-(id)init;
- (void) getClosestNodeWithLat:(double) lat lon:(double) lon completion:(void (^) (OVCResponse *resp, NSError *error))complete;
-(void) getPathFromNode:(NSString*)node1 toNode:(NSString*)node2 completion:(void (^) (OVCResponse *resp, NSError *error))complete;
-(void)getScheduleforUser:(NSString*)userID andToken:(NSString*)token completion:(void (^) (OVCResponse *resp, NSError *error))complete;
-(void)getNextClassForUser:(NSString*)userID andToken:(NSString*)token completion:(void (^) (OVCResponse *resp, NSError *error))complete;
-(void)getBuildings:(void (^) (OVCResponse *resp, NSError *error))complete;
@end
