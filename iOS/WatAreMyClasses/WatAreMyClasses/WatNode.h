//
//  WatNode.h
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Mantle/Mantle.h>

//Basic container for a Node

@interface WatNode : MTLModel<MTLJSONSerializing>

@property (nonatomic) NSString * ndid;
@property (nonatomic) NSString * lat;
@property (nonatomic) NSString * lon;
@property (nonatomic) NSString * name;

@end
