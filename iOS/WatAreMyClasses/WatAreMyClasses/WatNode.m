//
//  WatNode.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "WatNode.h"
//Basic container for a Node

@implementation WatNode

@synthesize ndid,lat,lon,name;

+ (NSDictionary *)JSONKeyPathsByPropertyKey {
    // properties defined in header < : > key in JSON Dictionary
    return @{
             @"ndid": @"id",
             @"lat":  @"lat",
             @"lon": @"lon",
             @"name": @"name",
             };
}

@end
