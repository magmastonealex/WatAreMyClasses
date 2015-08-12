//
//  DataCacher.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-11.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "DataCacher.h"

@implementation DataCacher
@synthesize classes;
@synthesize buildings;
@synthesize watService;
@synthesize userID;
@synthesize token;

+ (id)sharedCache {
    static DataCacher *sharedCache = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedCache = [[self alloc] init];
        sharedCache.watService=[WatService sharedService];
    });
    return sharedCache;
}
-(void)doCache{
    [watService getBuildings:^(OVCResponse *resp, NSError *error) {
        if(!error){
            NSLog(@"Sucessfully got buildings");
            buildings=[resp.result copy];
        }
    }];
    if(userID != nil){
        [watService getScheduleforUser:userID andToken:token completion:^(OVCResponse *resp, NSError *error) {
            if(!error){
                NSLog(@"Successfully got schedule");
                classes=[resp.result copy];
            }
        }];
    }
}

@end
