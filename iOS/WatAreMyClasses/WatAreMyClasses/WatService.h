//
//  WatService.h
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Overcoat/Overcoat.h>

@interface WatService : NSObject
-(id)init;
- (void) getClosestNodeWithLat:(float) lat lon:(float) lon completion:(void (^) (OVCResponse *resp, NSError *error))complete;

@end
